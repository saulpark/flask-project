# Codebase Audit Results

Audit date: 2026-02-24 (updated; original: 2026-02-16)
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
- **Status:** [x] Fixed — uses `url_for()` to generate correct URL.

### 7. No db.create_all() in app factory
- **Location:** `app/__init__.py`
- **Problem:** Tables are never created. Flask-Migrate is installed but not initialized. Fresh deployments fail.
- **Status:** [x] Fixed — `db.create_all()` called in app factory within `app_context()`.

### 18. No rate limiting on login endpoint
- **Location:** `app/auth/routes.py:10`
- **Problem:** No brute-force protection on `/auth/login`. An attacker can attempt unlimited password guesses against any account without being throttled or locked out.
- **Fix:** Use Flask-Limiter or similar to cap attempts (e.g., 10/minute per IP).
- **Status:** [ ] Pending

---

## Medium Issues

### 8. Bare except clauses
- **Location:** `app/notes/routes.py:58, 77, 157`
- **Problem:** Bare `except:` swallows all exceptions silently.
- **Fix:** Catch `json.JSONDecodeError` or `(ValueError, KeyError)` specifically.
- **Status:** [x] Fixed — now catches `(json.JSONDecodeError, KeyError, TypeError)`.

### 9. No max password length
- **Location:** `app/auth/forms.py`, `app/services/user_service.py:109`
- **Problem:** No upper bound on password length in either the form validators or the `update_password` service method. Very long passwords can cause a hashing DoS (bcrypt is O(n) in password length).
- **Fix:** Add `Length(max=128)` to form validators and `len(new_password) > 128` guard in service.
- **Status:** [ ] Pending

### 10. debug=True hardcoded
- **Location:** `run.py:6`
- **Problem:** Debug mode runs unconditionally. Must be environment-controlled in production.
- **Status:** [ ] Pending

### 11. share_note always regenerates token
- **Location:** `app/notes/services.py:150`
- **Problem:** Creates a new token every call, silently breaking existing shared links.
- **Fix:** Only generate token if `share_token is None`.
- **Status:** [x] Fixed — only generates token when `share_token` is falsy.

### 12. Public share URL path mismatch with tech spec
- **Tech spec ref:** Section 8.1 specifies `/p/<share_token>` but implementation uses `/notes/p/<token>`.
- **Status:** [ ] Pending

### 19. Cookie security settings not configured
- **Location:** `app/__init__.py`
- **Problem:** `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, and `SESSION_COOKIE_SAMESITE` are not set. In production over HTTP, session cookies can be stolen; without `SameSite`, CSRF attacks via subdomain are possible.
- **Fix:** Set `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE='Lax'` when not in testing.
- **Status:** [ ] Pending

### 20. No email normalization
- **Location:** `app/services/user_service.py:25-40`
- **Problem:** Email is stored and compared case-sensitively. `USER@Example.COM` and `user@example.com` are treated as different accounts, allowing duplicate registrations for the same address.
- **Fix:** Lowercase `email` before all storage and lookups.
- **Status:** [ ] Pending

### 21. Hardcoded SQLALCHEMY_DATABASE_URI
- **Location:** `app/__init__.py:6`
- **Problem:** Database URI is hardcoded to `sqlite:///notes.db`. Cannot be overridden per environment without code changes.
- **Fix:** Read from `os.environ.get('DATABASE_URL', 'sqlite:///notes.db')`.
- **Status:** [ ] Pending

### 22. CDN resources loaded without Subresource Integrity (SRI)
- **Location:** `app/templates/base.html:7-8`
- **Problem:** Bootstrap CSS and JS are loaded from jsDelivr CDN without `integrity` and `crossorigin` attributes. A CDN compromise could inject malicious scripts into all pages.
- **Fix:** Add SRI hashes (`integrity="sha384-..."`, `crossorigin="anonymous"`).
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
- **Location:** `app/users/routes.py:22`
- **Problem:** `len(user.notes)` loads all notes into memory to count them.
- **Fix:** Use a `count()` query.
- **Status:** [ ] Pending

### 17. Legacy Model.query API usage
- **Location:** `app/notes/services.py:72, 188`, `app/services/user_service.py:67, 146`
- **Problem:** Mixes `Note.query` / `User.query` (1.x style) with `db.session.get()` (2.0 style).
- **Fix:** Use `db.session.execute(db.select(...))` consistently.
- **Status:** [ ] Pending

### 23. run.py binds to 0.0.0.0 with debug enabled
- **Location:** `run.py:6`
- **Problem:** `host='0.0.0.0'` exposes the Flask debug server on all network interfaces. Combined with `debug=True`, the interactive debugger is reachable from the local network, allowing arbitrary code execution.
- **Fix:** Bind to `127.0.0.1` in development, or control via `HOST`/`DEBUG` env vars.
- **Status:** [ ] Pending

### 24. Dead service methods with no routes
- **Location:** `app/services/user_service.py:117-146`
- **Problem:** `UserService.delete_user()` and `UserService.get_all_users()` have no corresponding routes after the users blueprint was restricted. Dead code creates maintenance burden and confusion.
- **Fix:** Remove or mark clearly as internal/admin-only.
- **Status:** [ ] Pending

### 25. load_user integer conversion not guarded
- **Location:** `app/extensions.py:13`
- **Problem:** `int(user_id)` raises `ValueError` if the session contains a non-integer user_id (e.g., after a data migration or session tampering), causing a 500 error instead of a graceful logout.
- **Fix:** Wrap in try/except and return `None` on failure.
- **Status:** [ ] Pending

### 26. Orphan templates with no routes
- **Location:** `app/templates/users/list.html`, `app/templates/users/new.html`
- **Problem:** These templates exist but their corresponding routes were removed. They cause confusion and may reference undefined variables.
- **Fix:** Delete the orphan templates.
- **Status:** [ ] Pending

### 27. No custom error handlers
- **Location:** `app/__init__.py`
- **Problem:** No handlers registered for 403, 404, or 500 errors. Flask's generic error pages are shown, which are inconsistent with the app's Bootstrap UI and may expose stack traces in production.
- **Fix:** Register `@app.errorhandler(403/404/500)` handlers with branded templates.
- **Status:** [ ] Pending

### 28. Email existence checked before format validation
- **Location:** `app/services/user_service.py:25-31`
- **Problem:** `get_user_by_email()` is called before the email format is validated. An obviously malformed email still triggers a DB query, wasting a round-trip.
- **Fix:** Validate format first, then check for existing user.
- **Status:** [ ] Pending

### 29. LoginManager missing login_message_category
- **Location:** `app/extensions.py`
- **Problem:** `login_manager.login_message_category` is not set. The default flash category `'message'` does not map to any Bootstrap alert class, so the "Please log in" message may render unstyled.
- **Fix:** Set `login_manager.login_message_category = 'warning'`.
- **Status:** [ ] Pending

### 30. unshare_note does not clear share_token
- **Location:** `app/notes/services.py:173`
- **Problem:** `unshare_note` sets `is_shared = False` but leaves `share_token` intact. Re-sharing the note will reactivate the same (previously distributed) link rather than generating a fresh token. Users expecting a new private link after revoking access will be surprised.
- **Fix:** Clear `share_token = None` on unshare, so the next share always generates a new token.
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
- **Note ownership:** `_get_own_note_or_404()` enforced on all note mutation routes.
- **User profile isolation:** `_ensure_own_user()` enforced on all user routes.

---

## Tech Spec Milestone Status

| Milestone | Status | Notes |
|---|---|---|
| DB models + migrations | Done | Models done, `db.create_all()` wired in app factory |
| Auth (register/login/logout) | Done | Open redirect fixed |
| Notes CRUD | Done | Ownership authorization added |
| Quill.js integration | Not started | Still using plain textarea |
| Sharing via token | Done | URL and token regeneration fixed |
| CSRF / security hardening | Partial | CSRF done; note & user authorization added; open redirect fixed; rate limiting, cookie flags, SRI pending |
| UX polish (Bootstrap) | Done | |
| Test coverage | Done | 82 tests: auth routes, note ownership, user restrictions, services |
