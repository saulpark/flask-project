# Codebase Audit Results

Audit date: 2026-02-16
Evaluated against: [TECH-SPEC.MD](TECH-SPEC.MD) and official library documentation.

---

## Critical Issues

### 1. No note ownership checks
- **Location:** `app/notes/routes.py` (all routes)
- **Problem:** `get_note_by_id(id)` never verifies `note.user_id == current_user.id`. Any authenticated user can view, edit, delete, share, or unshare any note by guessing an integer ID.
- **Tech spec ref:** Section 6.3 — "Only the owner can view private notes, edit/update/delete, share/unshare."
- **Status:** [x] Fixed — `_get_own_note_or_404()` helper checks ownership; returns 403 if not owner.

### 2. No authorization on users blueprint
- **Location:** `app/users/routes.py` (all routes)
- **Problem:** Any authenticated user can list all users, view any profile, change any user's password, and delete any user. No admin role or ownership check exists.
- **Status:** [x] Fixed — removed list/create/delete routes; view and password restricted to own user via `_ensure_own_user()`.

### 3. Open redirect on login
- **Location:** `app/auth/routes.py:18-19`
- **Problem:** `next_page = request.args.get('next')` is used without validation. An attacker can craft `?next=https://evil.com` to redirect users off-site after login.
- **Fix:** Validate that `next` is a relative URL (e.g., check `url_parse(next_page).netloc == ''`).
- **Status:** [x] Fixed — rejects `next` URLs with a netloc (external hosts).

### 4. Hardcoded SECRET_KEY
- **Location:** `app/__init__.py:5`
- **Problem:** `SECRET_KEY` is hardcoded as `'dev-secret-key-change-in-production'`. No `config.py` exists for environment separation.
- **Tech spec ref:** Section 14 — config via environment variables.
- **Status:** [ ] Pending

---

## High Issues

### 5. JSON injection via f-string
- **Location:** `app/notes/routes.py:34, 95`
- **Problem:** Content is interpolated into JSON with an f-string. If content contains `"`, `\`, or newlines, it produces malformed or exploitable JSON.
- **Fix:** Use `json.dumps()` to safely serialize content.
- **Status:** [x] Fixed — replaced f-string with `json.dumps()`.

### 6. Wrong public share URL in flash message
- **Location:** `app/notes/routes.py:125`
- **Problem:** Flash shows `{request.host_url}p/{token}` but the route is at `/notes/p/<token>`.
- **Fix:** Use `url_for('notes.public_note', token=token, _external=True)`.
- **Status:** [ ] Pending

### 7. No db.create_all() in app factory
- **Location:** `app/__init__.py`
- **Problem:** Tables are never created. Flask-Migrate is installed but not initialized. Fresh deployments fail.
- **Status:** [ ] Pending

---

## Medium Issues

### 8. Bare except clauses
- **Location:** `app/notes/routes.py:58, 77, 157`
- **Problem:** Bare `except:` swallows all exceptions silently.
- **Fix:** Catch `json.JSONDecodeError` or `(ValueError, KeyError)` specifically.
- **Status:** [x] Fixed — now catches `(json.JSONDecodeError, KeyError, TypeError)`.

### 9. No max password length
- **Location:** `app/auth/forms.py`
- **Problem:** No upper bound on password length. Very long passwords can cause a hashing DoS.
- **Fix:** Add `Length(max=128)` to password validators.
- **Status:** [ ] Pending

### 10. debug=True hardcoded
- **Location:** `run.py`
- **Problem:** Debug mode runs unconditionally. Must be environment-controlled in production.
- **Status:** [ ] Pending

### 11. share_note always regenerates token
- **Location:** `app/notes/services.py:150`
- **Problem:** Creates a new token every call, silently breaking existing shared links.
- **Fix:** Only generate token if `share_token is None`.
- **Status:** [ ] Pending

### 12. Public share URL path mismatch with tech spec
- **Tech spec ref:** Section 8.1 specifies `/p/<share_token>` but implementation uses `/notes/p/<token>`.
- **Status:** [ ] Pending

---

## Low Issues

### 13. Unused dependency: peewee
- **Location:** `requirements.txt`
- **Fix:** Remove `peewee==3.19.0`.
- **Status:** [ ] Pending

### 14. sqlite-web in main requirements
- **Location:** `requirements.txt`
- **Problem:** Dev/Docker tool should not be a runtime dependency.
- **Status:** [ ] Pending

### 15. import json inside functions
- **Location:** `app/notes/routes.py:54, 74, 154`
- **Fix:** Move to top-level import.
- **Status:** [x] Fixed — moved to top-level import.

### 16. Inefficient note count query
- **Location:** `app/users/routes.py:56`
- **Problem:** `len(user.notes)` loads all notes into memory to count them.
- **Fix:** Use a `count()` query.
- **Status:** [ ] Pending

### 17. Legacy Model.query API usage
- **Location:** `app/notes/services.py:72, 188`, `app/services/user_service.py`
- **Problem:** Mixes `Note.query` (1.x style) with `db.session.get()` (2.0 style).
- **Fix:** Use `db.session.execute(db.select(...))` consistently.
- **Status:** [ ] Pending

---

## What's Working Correctly

- **CSRF protection:** All POST forms include tokens, `CSRFProtect` initialized globally.
- **Templates / XSS:** Jinja2 auto-escaping active, `| safe` never used on user data.
- **Bootstrap 5:** Correctly used throughout (BS5 `data-bs-*` attributes, proper utility classes).
- **url_for prefixes:** Correct in all templates.
- **Flash messages:** Properly handled in `base.html` with Bootstrap alert categories.
- **Password hashing:** Werkzeug used correctly in User model.
- **Logout:** POST-only (correct).
- **Content size validation:** 2MB limit enforced in service layer.
- **Share token generation:** `secrets.token_urlsafe(32)` — cryptographically secure.

---

## Tech Spec Milestone Status

| Milestone | Status | Notes |
|---|---|---|
| DB models + migrations | Partial | Models done, no `db.create_all()` or migrations wired |
| Auth (register/login/logout) | Done | Open redirect fixed |
| Notes CRUD | Done | Ownership authorization added |
| Quill.js integration | Not started | Still using plain textarea |
| Sharing via token | Done | Wrong URL + token regeneration issue |
| CSRF / security hardening | Partial | CSRF done; note & user authorization added; open redirect fixed |
| UX polish (Bootstrap) | Done | |
