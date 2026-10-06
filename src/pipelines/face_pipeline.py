
import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 


    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings= []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding

        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def _distance_to_confidence(distance, threshold=0.6):
    """Converts an L2 embedding distance into an approximate 0-100 match
    confidence. This is a simple derived score for display purposes
    (closer embeddings => higher %), not a calibrated probability."""
    conf = (1 - (distance / (threshold * 2))) * 100
    return round(max(0.0, min(100.0, conf)), 1)


def predict_attendance(class_image_np, resemblance_threshold=0.6):
    if resemblance_threshold <= 0:
        raise ValueError("The face match threshold must be greater than zero.")

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}


    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students)>= 2:
            predicted_id= int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)]

        best_match_score = np.linalg.norm(student_embedding - encoding)

        if best_match_score <= resemblance_threshold:
            confidence = _distance_to_confidence(best_match_score, resemblance_threshold)
            # Keep the highest confidence if this student was already matched
            # in this same image (shouldn't normally happen, but safe).
            existing = detected_student.get(predicted_id, 0)
            detected_student[predicted_id] = max(existing, confidence)
    return detected_student, all_students, len(encodings)
