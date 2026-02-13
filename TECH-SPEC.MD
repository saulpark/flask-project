# Note Taking Web App — Technical Specification (Flask)

## 1. Overview

### 1.1 Purpose
Build a web app where authenticated users can create and manage rich-text notes. Notes can optionally be shared publicly via a link and later unshared.

### 1.2 Core features
- Create, view, update, delete (CRUD) notes
- Public sharing on/off per note
- Rich text editing:
  - Bold, italic
  - Inline code + code blocks/snippets
  - Bullet lists
  - Horizontal separator lines

### 1.3 Tech stack
- **Backend:** Python + Flask
- **DB:** SQLite
- **ORM:** SQLAlchemy
- **Auth:** Flask-Login (session-based)
- **Styling:** Bootstrap 5
- **Rich text editor:** Quill.js (frontend), store Quill Delta JSON in DB

## 2. Assumptions / Decisions (explicit)
These assumptions can be changed later, but the spec is written for:

- Notes are owned by exactly one user
- Public sharing is "anyone with the link" (not indexed)
- Public notes are read-only for anonymous viewers
- Authentication is email + password (no OAuth in v1)
- Content is stored as Quill Delta JSON (source of truth)

## 3. Non-functional requirements
- **Security:** password hashing, CSRF protection for forms, strict authorization checks
- **Reliability:** migrations supported (even with SQLite)
- **Maintainability:** clear project structure, service boundaries, tests for critical logic
- **Performance:** suitable for small/medium personal/team usage; SQLite acceptable for v1

## 4. Architecture

### 4.1 High-level design
Server-rendered Flask app using Jinja templates:

- Flask serves HTML pages
- Quill editor runs in the browser
- On save/update, browser sends note content as JSON (Quill Delta) to Flask
- Flask validates and persists via SQLAlchemy into SQLite

### 4.2 Suggested project structure
```
app/
  __init__.py
  config.py
  extensions.py        # db, login manager, csrf, etc.
  models.py
  auth/
    routes.py
    forms.py
  notes/
    routes.py
    forms.py           # if using WTForms
    services.py        # note creation/update/share logic
  templates/
    base.html
    auth/
    notes/
  static/
    css/
    js/
migrations/
tests/
run.py
```
## 5. Data model (SQLite + SQLAlchemy)

### 5.1 Tables

#### users
- `id` (PK, integer)
- `email` (unique, indexed, not null)
- `password_hash` (not null)
- `created_at` (not null)
- `updated_at` (not null)

#### notes
- `id` (PK, integer)
- `user_id` (FK -> users.id, indexed, not null)
- `title` (string, optional; can be derived or user-entered)
- `content_delta` (JSON/text, not null)
  - Store Quill Delta as JSON string (SQLite doesn't have a strict JSON type; SQLAlchemy can store as Text)
- `is_shared` (boolean, default false)
- `share_token` (string, unique, nullable)
  - Random unguessable token for public link
- `created_at` (not null)
- `updated_at` (not null)

### 5.2 SQLAlchemy model sketch

```python
# models.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    notes = db.relationship("Note", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)

    title = db.Column(db.String(200), nullable=True)
    content_delta = db.Column(db.Text, nullable=False)

    is_shared = db.Column(db.Boolean, default=False, nullable=False)
    share_token = db.Column(db.String(64), unique=True, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="notes")
```
## 6. Authentication & Authorization

### 6.1 Authentication
Flask-Login provides session handling:

- Login route sets session
- Logout clears session
- `@login_required` protects note management routes

### 6.2 User loader

```python
# extensions.py or auth setup
from flask_login import LoginManager
from app.extensions import db

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))
```

### 6.3 Authorization rules

**Only the owner can:**
- View private note pages
- Edit/update/delete a note
- Share/unshare a note

**Public route:**
- Anyone can view a note only if `is_shared = True` and token matches

## 7. Rich Text Editor (Quill)

### 7.1 Editor integration
- Load Quill JS + CSS in templates
- Provide a div container for the editor
- On save:
  - Read editor contents: `quill.getContents()` (Delta)
  - Send JSON delta to backend

### 7.2 Delta storage
- Store Delta JSON string in `notes.content_delta`
- When rendering:
  - For authenticated owner view/edit: load delta back into Quill `quill.setContents(delta)`
  - For public view: either render via Quill in read-only mode, or convert Delta to HTML on server (v2 improvement)

### 7.3 Formatting requirements mapping
- **Bold/italic:** native Quill formats
- **Bullet lists:** native
- **Inline code:** Quill supports code inline format
- **Code blocks:** supported via code-block format (ensure toolbar includes it)
- **Horizontal rule:** may require a custom embed/blot; include as v1.1 if you want to keep v1 simpler

## 8. UI/UX (Bootstrap 5)

### 8.1 Pages

**Auth:**
- `/register` (email, password, confirm)
- `/login` (email, password)
- `/logout`

**Notes (authenticated):**
- `/notes` - list page (title, updated time, share status)
- `/notes/new` - create page
- `/notes/<id>` - view page
- `/notes/<id>/edit` - edit page

**Public:**
- `/p/<share_token>` - public read-only view

### 8.2 Components
- **Navbar:** app name, "My Notes", "New Note", user menu
- **Notes list:** table or cards, actions: View/Edit/Delete/Share
- **Flash messages** for success/error

## 9. API / Routes specification

### 9.1 Auth routes
- `GET /register` → show register form
- `POST /register` → create user, log in, redirect to /notes
- `GET /login` → show login form
- `POST /login` → authenticate, log in, redirect
- `POST /logout` → log out, redirect to /login

### 9.2 Notes routes (HTML forms or JSON)

**Option A: classic form posts (simple):**
- `GET /notes`
- `GET /notes/new`
- `POST /notes` (create)
- `GET /notes/<id>`
- `GET /notes/<id>/edit`
- `POST /notes/<id>` (update)
- `POST /notes/<id>/delete` (delete)
- `POST /notes/<id>/share` (toggle on; creates token)
- `POST /notes/<id>/unshare` (toggle off; invalidates token)

**Option B: JSON endpoints (cleaner for Quill autosave):**
- `POST /api/notes` (create)
- `PUT /api/notes/<id>` (update)
- `DELETE /api/notes/<id>` (delete)
- `POST /api/notes/<id>/share`
- `POST /api/notes/<id>/unshare`

**Recommendation:** start with Option A and only add JSON endpoints if you implement autosave.

### 9.3 Public route
- `GET /p/<token>` → render shared note read-only if valid, else 404

## 10. Note sharing design

### 10.1 Token generation

**When sharing is enabled:**
- `is_shared = True`
- Create `share_token = secrets.token_urlsafe(32)` (or similar)

**When unsharing:**
- `is_shared = False`
- Set `share_token = NULL` (or rotate token)

### 10.2 Public visibility
- No directory listing of shared notes
- Token must be unguessable; treat link as secret

## 11. Validation & Error handling

**Validate input:**
- Email format, password length
- Note delta must be valid JSON; enforce max size (e.g., 1–2 MB)

**Error behavior:**
- Unauthorized access → 403 or redirect to login (depending on route type)
- Note not found / token invalid → 404
- CSRF failures → 400

## 12. Security requirements (v1)

- Password hashing using Werkzeug
- CSRF protection for all state-changing requests (POST/PUT/DELETE)
- Secure session cookie settings in production:
  - `SESSION_COOKIE_SECURE=True`
  - `SESSION_COOKIE_HTTPONLY=True`
  - `SESSION_COOKIE_SAMESITE='Lax'` (or Strict depending on needs)
- Output encoding:
  - For public view, avoid injecting raw HTML from user input unless sanitized
  - Prefer rendering via Quill in read-only mode to reduce XSS risk (still be cautious)

## 13. Testing plan

**Unit tests:**
- Auth: register/login/logout
- Authorization: cannot access others' notes
- Sharing: token creation, public access, unshare invalidates access

**Integration tests:**
- CRUD flows end-to-end

**Basic security tests:**
- CSRF on destructive actions
- Session protection on private routes

## 14. Deployment notes (simple)

**Config via environment variables:**
- `SECRET_KEY`
- `DATABASE_URL` (or SQLite path)

**Production setup:**
- Use a WSGI server (e.g., gunicorn) behind a reverse proxy (e.g., nginx) for production
- SQLite is fine for a single-instance deployment; move to Postgres if scaling

## 15. Milestones

1. Project scaffolding + DB models + migrations
2. Auth (register/login/logout)
3. Notes CRUD (plain textarea first)
4. Quill integration + Delta JSON storage
5. Sharing via token route
6. Hardening: CSRF, security headers, basic tests
7. UX polish (Bootstrap), empty states, flash messages