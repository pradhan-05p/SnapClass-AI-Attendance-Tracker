# SnapClass-AI-Attendance-Tracker

An attendance management system built to remove the most tedious part of a teacher's day — calling out roll numbers one by one and manually noting who's present. Instead, students are marked present through face recognition, and teachers get a dashboard to view, filter, and export attendance logs per subject and per date.

This project started as an idea from the **Apna College AI Dev module**, and grew from there into a full-stack app with authentication, a recognition ML pipeline, and a teacher-facing dashboard.

---

## Problem It Solves

In a normal classroom, taking attendance manually:
- Eats up 5–10 minutes of every class calling out names/roll numbers
- Is error-prone (skipped names, marked-present-by-mistake, proxy attendance)
- Leaves no easy way to look back at a student's attendance history without digging through registers

This app solves that by:
- Marking students present via face recognition, cutting down manual roll-calls
- Giving teachers a searchable, filterable attendance log (by date + subject) instead of a paper register
- Making it easy to pull up any single student's attendance history on demand

**Impact:** less classroom time lost to admin work, fewer manual errors, and attendance data that's actually easy to query later — for teachers, parents, or the institution.

---

## Tech Stack

- **Frontend/App:** Python + Streamlit
- **Face/Voice Recognition:** `resemblyzer`, `librosa`, `numpy` (embeddings stored per student)
- **Backend/DB:** Supabase
- **Auth:** Plain username/password check against the `teachers` table — no Supabase Auth
- **Data handling:** `pandas`

---

## Core Features

- **Student attendance marking** — face recognition against stored embeddings, no manual roll call needed
- **Teacher login** — username/password checked directly against the `teachers` table
- **Teacher dashboard**
  - Select a subject (via a selectbox, populated from the subjects the teacher teaches)
  - Select a date
  - View a table of every enrolled student for that subject with **Present/Absent** status and the timestamp they were marked
  - Download the log as CSV
  - **Refresh button** to re-pull the latest data without restarting the app
  - **Per-student logs view** — see a single student's attendance history across all sessions, not just one day

---

## Database Schema

- **`students`** — `student_id`, `name`, `face_embeddings` (jsonb), `voice_embeddings` (jsonb)
- **`teachers`** — `teacher_id`, `username`, `password`, `name`
- **`subjects`** — `subject_id`, `subject_code`, `name`, `section`, `teacher_id`
- **`subject_students`** — join table: `subject_id`, `student_id`
- **`attendance_logs`** — `id`, `timestamp` (timestamptz), `subject_id`, `student_id`, `ispresent` (bool)

---

## Honest Build Log — The Bug That Actually Cost Time

Most of the small stuff (typos, table-name mismatches, an indentation error here and there) got fixed in minutes and isn't worth documenting — normal parts of building anything.

The one that actually mattered:

### The recognition pipeline
The face/voice recognition pipeline caused serious, hard-to-pin-down problems and ate up **at least 4 days of debugging**. Unlike the small syntax/naming issues, this wasn't a quick fix — it was the core of the project not behaving reliably, and getting it stable took sustained trial and error rather than a single "aha" fix.

### How it got solved
- The recognition pipeline debugging was worked through directly, since it required understanding the embeddings/model behavior rather than reading an error message and patching one line.
- **Claude** was used to help design the dashboard query logic — joining `students` → `subject_students` → `attendance_logs`, and merging with pandas to fill in "Absent" for students with no log row for a given date — and to rewrite that code as the actual schema became clear.
- **ChatGPT** was used for debugging recurring/frequent errors and for brainstorming feature extensions — specifically the idea to add a **refresh button** and a **per-student detailed logs view**, which weren't part of the original scope.

---

## Future Scope

- Attendance analytics (attendance % trends per student/subject over time)
- Notifications to parents/students below an attendance threshold
- Bulk CSV export across a whole date range, not just one day

---

## Credits

- Project idea originated from the **Apna College AI Dev module**
- Built and debugged by **Prateek Pradhan**, with AI assistance (Claude, ChatGPT) used for query design, debugging support, and feature-extension ideas
