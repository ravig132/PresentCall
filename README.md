# Present Call - AI Intelligent Attendance System

Present Call eliminates manual roll calls and proxy attendance using AI-powered
face and voice recognition. A teacher captures one group photo (or one
classroom audio clip), and the system automatically detects, matches, and
logs every present student - no calling names, no impersonation.

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
- **Light/Dark theme toggle**, consistent navigation, and a unified design
  system across every page.

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

## 📁 Project Structure

```
PresentCall/
├── app.py                          # Entry point & routing
├── requirements.txt
├── assets/
│   └── favicon.png                 # App logo / favicon
├── .streamlit/
│   └── secrets.toml                # Supabase credentials (NOT committed)
└── src/
    ├── ui/
    │   └── base_layout.py          # Theme system, global CSS, fonts
    ├── components/
    │   ├── navbar.py                # Persistent top navigation bar
    │   ├── header.py                # Hero header (Home page)
    │   ├── footer.py                # Site-wide footer
    │   ├── subject_card.py          # Subject display card
    │   ├── dialog_add_photo.py
    │   ├── dialog_attendance_results.py
    │   ├── dialog_auto_enroll.py
    │   ├── dialog_create_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_share_subject.py
    │   └── dialog_voice_attendance.py
    ├── screens/
    │   ├── home_screen.py           # Landing page
    │   ├── about_screen.py          # About / workflow explanation
    │   ├── student_screen.py        # Student login + dashboard
    │   └── teacher_screen.py        # Teacher login + dashboard
    ├── pipelines/
    │   ├── face_pipeline.py         # Face detection, embedding, matching
    │   └── voice_pipeline.py        # Voice embedding, speaker matching
    └── database/
        ├── config.py                # Supabase client init
        └── db.py                    # All database queries
```

---

## ⚙️ Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url> PresentCall
cd PresentCall
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install resemblyzer --no-deps
```

### 3. Create a Supabase project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Open **SQL Editor → New query**, paste in the contents of
   `presentcall_schema.sql`, and run it. This creates all five tables
   (`teachers`, `students`, `subjects`, `subject_students`,
   `attendance_logs`) with the correct columns, foreign keys, and
   permissive RLS policies
3. Go to **Settings → API Keys** and copy:
   - Your **Project URL** (Settings → General → Project ID →
     `https://<project-id>.supabase.co`)

### 4. Configure secrets

Create `.streamlit/secrets.toml` in the project root:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "sb_publishable_..."
```

Add this file to `.gitignore` - it should never be committed.

### 5. Run the app

```bash
streamlit run app.py
```

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

## 🙏 Credits

Designed by **[P-Vijay](https://p-vijay.vercel.app/)** with a cup of tea 🍵
[License](LICENSE)