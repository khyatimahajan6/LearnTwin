
# LearnTwin AI Professor — Input Processing & File Handling Backend

This is the **Member 1** backend for the *LearnTwin AI Professor* Final Year Project.
It is responsible for:

- Student authentication (register/login) with SQLite + SQLAlchemy
- Uploading lecture files (PDF / DOCX / PPTX)
- Detecting file type and extracting text (PyMuPDF, python-docx, python-pptx)
- Merging extracted text and saving it to disk
- Tracking upload/processing history per student
- Robust validation, error handling, and logging

Built with **FastAPI**, following clean, modular architecture so other
team members (Member 2: AI processing, Member 3: frontend, etc.) can
plug straight into this API.

---

## 1. Project Structure

```
learntwin-backend/
├── postman_collection.json       # Import into Postman to test every endpoint
├── README.md                     # This file
└── backend/
    ├── main.py                   # FastAPI app entry point
    ├── config.py                 # All constants (paths, limits, secrets)
    ├── requirements.txt          # Python dependencies
    ├── learntwin.db               # SQLite database (auto-created on first run)
    │
    ├── database/
    │   ├── db.py                 # SQLAlchemy engine/session setup
    │   └── schema.sql            # Reference SQL schema (documentation)
    │
    ├── models/                   # SQLAlchemy ORM models (DB tables)
    │   ├── student.py
    │   └── lecture.py
    │
    ├── schemas/                  # Pydantic models (API request/response shapes)
    │   ├── auth_schema.py
    │   └── lecture_schema.py
    │
    ├── routes/                   # FastAPI route handlers (HTTP layer)
    │   ├── auth_routes.py
    │   ├── upload_routes.py
    │   └── history_routes.py
    │
    ├── services/                 # Business logic (framework-independent)
    │   ├── auth_service.py
    │   ├── file_service.py
    │   ├── extraction_service.py
    │   └── lecture_service.py
    │
    ├── utils/                    # Shared helpers
    │   ├── logger.py
    │   └── validators.py
    │
    ├── uploads/                  # Raw uploaded files land here
    ├── extracted_text/           # Extracted .txt files land here
    └── logs/                     # app.log (rotating log file)
```

### Why this structure? (Clean Architecture)

| Layer        | Folder       | Responsibility                                          |
|--------------|-------------|-----------------------------------------------------------|
| Presentation | `routes/`    | Handles HTTP requests/responses only — no business logic |
| Application  | `services/`  | All business logic, reusable, framework-independent      |
| Domain       | `models/`    | Database table definitions (SQLAlchemy ORM)               |
| Contracts    | `schemas/`   | Defines the JSON shape of requests/responses (Pydantic)    |
| Support      | `utils/`     | Cross-cutting helpers (logging, validation)                |

This separation means: if you swap FastAPI for Flask tomorrow, only
`routes/` needs to change. If you swap SQLite for PostgreSQL, only
`config.py`/`database/db.py` need to change.

---

## 2. Setup & Run

```bash
cd backend
pip install -r requirements.txt

# Start the development server (auto-reloads on code changes)
uvicorn main:app --reload
```

Then open:
- **Swagger UI (interactive docs)**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

The SQLite database file (`learntwin.db`) and the `uploads/`,
`extracted_text/`, `logs/` folders are created automatically on first run.

---

## 3. API Endpoints

| Method | Endpoint             | Auth required | Description                                  |
|--------|-----------------------|:--------------:|-----------------------------------------------|
| GET    | `/`                    | No             | Health check                                  |
| POST   | `/auth/register`       | No             | Create a new student account, returns JWT     |
| POST   | `/auth/login`          | No             | Log in, returns JWT                           |
| POST   | `/upload`              | **Yes**         | Upload a PDF/DOCX/PPTX, extract & merge text  |
| GET    | `/history`             | **Yes**         | List the logged-in student's upload history   |
| GET    | `/history/{lecture_id}`| **Yes**         | Get details of a single upload                |

All protected routes expect:
```
Authorization: Bearer <access_token>
```
(the token you receive from `/auth/register` or `/auth/login`)

### Example: `POST /upload` response

```json
{
  "lecture_id": "8454dc94-20aa-4a22-903a-702c4d6d1db0",
  "filename": "test.pdf",
  "file_type": "pdf",
  "raw_text": "--- Page 1 ---\nLecture content here...",
  "status": "Processed"
}
```

### Example: `GET /history` response

```json
[
  {
    "lecture_id": "8454dc94-20aa-4a22-903a-702c4d6d1db0",
    "student_id": "38fcd640-b3c5-4b2b-b08d-ad45888cb3db",
    "filename": "test.pdf",
    "file_type": "pdf",
    "file_size_kb": 1,
    "page_count": 2,
    "upload_time": "2026-08-07T11:41:45.404664",
    "processing_status": "Completed",
    "error_message": null
  }
]
```

---

## 4. File Validation Rules

Enforced in `utils/validators.py` before any file touches the database or disk:

- ✅ Allowed types only: `.pdf`, `.docx`, `.pptx`
- ✅ Maximum size: **20 MB**
- ✅ Empty files (0 bytes) rejected
- ✅ Corrupted / unreadable files are caught during extraction and marked
  `Failed` in the history table (with an `error_message`), instead of
  crashing the server

| Scenario                  | HTTP Status | Example detail message                                  |
|----------------------------|:-----------:|-----------------------------------------------------------|
| Unsupported file type      | 400         | "File type '.txt' is not supported..."                    |
| Empty file                 | 400         | "The uploaded file is empty."                              |
| File too large             | 400         | "File is too large (25.30 MB). Maximum allowed is 20 MB." |
| Corrupted file content     | 422         | "Failed to process file: Could not open PDF file..."      |
| No/invalid auth token      | 401         | "Could not validate credentials."                          |

---

## 5. Processing Status Lifecycle

Every uploaded lecture moves through these statuses (stored in the
`lectures.processing_status` column):

```
Uploading  →  Extracting  →  Completed
                    ↘
                     Failed   (if the file is corrupted/unreadable)
```

---

## 6. Database Schema

See [`backend/database/schema.sql`](backend/database/schema.sql) for the
full reference SQL. Summary:

**students**
| Column           | Type     | Notes                        |
|------------------|----------|-------------------------------|
| id               | INTEGER  | Primary key                   |
| student_id       | VARCHAR  | Public UUID (used in JWT)     |
| full_name        | VARCHAR  |                                |
| email            | VARCHAR  | Unique, used for login        |
| hashed_password  | VARCHAR  | Bcrypt hash                   |
| created_at       | DATETIME |                                |

**lectures**
| Column               | Type     | Notes                                   |
|----------------------|----------|-------------------------------------------|
| id                   | INTEGER  | Primary key                               |
| lecture_id           | VARCHAR  | Public UUID                               |
| student_id           | VARCHAR  | FK → students.student_id                  |
| filename             | VARCHAR  |                                            |
| file_type            | VARCHAR  | pdf / docx / pptx                         |
| file_size_kb         | INTEGER  |                                            |
| page_count           | INTEGER  | Nullable (not all DOCX have a page count) |
| upload_time          | DATETIME |                                            |
| processing_status    | VARCHAR  | Uploading / Extracting / Completed / Failed |
| extracted_text_path  | VARCHAR  | Path to the saved .txt file               |
| error_message        | TEXT     | Populated only when status = Failed       |

**Relationship:** One student → many lectures (`students.student_id` = `lectures.student_id`)

---

## 7. Testing with Postman

Import [`postman_collection.json`](postman_collection.json) into Postman.
It includes requests for:

1. Health Check
2. Auth → Register Student (auto-saves the JWT token to a collection variable)
3. Auth → Login Student
4. Upload → Upload PDF/DOCX/PPTX (attach a file in the `file` form field)
5. History → Get All Upload History
6. History → Get Single Lecture by ID

The collection automatically stores `access_token` and `lecture_id` as
variables after successful requests, so you don't need to copy/paste
them manually between requests.

---

## 8. Logging

All modules log through `utils/logger.py`, which writes to both the
console and a rotating log file at `backend/logs/app.log`. Every
upload, extraction step, validation failure, and error is logged with
a timestamp — useful for debugging and for demonstrating the pipeline
during your project viva/demo.

---

## 9. Notes for the Team

- This backend returns `raw_text` directly in the `/upload` response,
  so **Member 2 (AI processing)** can immediately feed it into their
  summarization/Q&A pipeline without needing a separate fetch call.
- The extracted `.txt` files are also persisted in `extracted_text/`,
  keyed by `lecture_id`, in case Member 2's pipeline needs to reprocess
  text later without re-uploading the original file.
- CORS is currently open (`allow_origins=["*"]`) for easy local frontend
  development — restrict this to your actual frontend domain before
  deploying to production.


