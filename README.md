# Present Call - AI Intelligent Attendance System

Present Call eliminates manual roll calls and proxy attendance using AI-powered
face and voice recognition. A teacher captures one group photo (or one
classroom audio clip), and the system automatically detects, matches, and
logs every present student - no calling names, no impersonation

---

## ✨ Features

- **QR-based self-enrollment** - students scan a subject QR code and enroll
  with a selfie (and optionally a voice sample).
- **One-photo attendance** - teachers upload/capture a single group photo;
  the backend detects every face, matches it against the class roster, and
  deduplicates repeat detections automatically.
- **Voice attendance** - an alternative flow using speaker recognition on a
  single classroom audio recording.
- **Dual dashboards** - separate, purpose-built views for teachers and
  students.
- **Live attendance analytics** - subject-wise attendance percentage,
  history, and records for both roles.
- **Teacher operations and management** - dashboard with recent verification
  activity, AI face attendance, VoiceID roll-call, detailed attendance
  records, student directory, subject management, and a session-persistent
  face match threshold.
- **Student portal** - dashboard, subject-wise attendance, detailed attendance
  records, and biometric enrollment status.
- **Attendance exports** - one detailed CSV export with student, subject,
  teacher, timestamp, method, confidence, and status fields.
- **Light/Dark theme toggle**, consistent navigation, and a unified design
  system across every page.

---

## Database migration

Before using verification methods and confidence in attendance records, run
[`migrations/20261006_attendance_verification_metadata.sql`](./migrations/20261006_attendance_verification_metadata.sql)
against the Supabase database. It adds nullable `method` and `confidence`
columns to `attendance_logs`, so existing records remain valid. Face and voice
attendance will then store the method and a distance/similarity-derived score;
these scores are estimates, not calibrated probabilities.

---


## 🧱 Tech Stack

| Layer              | Technology                                      |
|---------------------|--------------------------------------------------|
| Frontend / App       | Streamlit                |
| Backend              | Python, Fast APIs                                 |
| Database             | Supabase (PostgreSQL)     |
| Face Detection & ID  | `dlib`, `face_recognition_models`, `scikit-learn` (SVM classifier) |
| Voice Recognition    | Resemblyzer, `librosa` |
| Auth                 | `bcrypt` (password hashing)               |
| QR Codes             | `segno`                                           |

---

## 🧠 How Attendance Matching Works

1. A teacher captures a group photo or classroom audio clip.
2. **Face path:** `RetinaFace`-style detection (via `dlib`) locates every
   face; each is converted into a 128-dimension embedding and compared
   against the enrolled class roster using a trained SVM classifier plus
   a distance-based sanity check.
3. **Voice path:** the audio is segmented by voice activity; each segment
   is embedded via `Resemblyzer` and matched against enrolled students'
   stored voice embeddings using cosine similarity.
4. Duplicate detections of the same student within one session are
   automatically deduplicated - each present student is logged exactly
   once.
5. Results are shown to the teacher for review before being saved to
   `attendance_logs`.

---

## 🚧 Known Limitations / Roadmap

- No liveness detection yet - a printed photo can currently be used to
  spoof face recognition. Planned for a future phase.
- Voice attendance accuracy drops in noisy or overlapping classroom audio.
- Large classes (60+ students) in one photo may reduce per-face
  resolution and accuracy.
- Responsive design has been tested at a few breakpoints but not
  exhaustively across all devices.

---
