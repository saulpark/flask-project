# Audit Log

Tracks the history of issues opened and resolved in [AUDIT.md](AUDIT.md).

---

## Issues Resolved

| Issue # | Title | Resolved Date | Resolved By | Commit(s) |
|---------|-------|--------------|-------------|-----------|
| 1 | No note ownership checks | 2026-02-17 | Saul P (saulpark@hotmail.com) | `85da960` |
| 2 | No authorization on users blueprint | 2026-02-17 | Saul P (saulpark@hotmail.com) | `85da960` |
| 3 | Open redirect on login | 2026-02-17 | Saul P (saulpark@hotmail.com) | `491e6f4` |
| 5 | JSON injection via f-string | 2026-02-17 | Saul P (saulpark@hotmail.com) | `2a3a841` |
| 6 | Wrong public share URL in flash message | 2026-02-17 | Saul P (saulpark@hotmail.com) | `2a3a841` |
| 7 | No db.create_all() in app factory | 2026-02-17 | Saul P (saulpark@hotmail.com) | `2a3a841` |
| 8 | Bare except clauses | 2026-02-17 | Saul P (saulpark@hotmail.com) | `d05dcae` |
| 11 | share_note always regenerates token | 2026-02-17 | Saul P (saulpark@hotmail.com) | `ceb9e33` |
| 15 | import json inside functions | 2026-02-17 | Saul P (saulpark@hotmail.com) | `d05dcae` |

---

## Issues Currently Open (as of 2026-02-24)

| Issue # | Title | Severity | Opened Date | Opened By |
|---------|-------|----------|------------|-----------|
| 4 | Hardcoded SECRET_KEY | Critical | 2026-02-16 | Saul P |
| 9 | No max password length (form + service) | Medium | 2026-02-16 | Saul P |
| 10 | debug=True hardcoded in run.py | Medium | 2026-02-16 | Saul P |
| 12 | Public share URL path mismatch with tech spec | Medium | 2026-02-16 | Saul P |
| 13 | Unused dependency: peewee | Low | 2026-02-16 | Saul P |
| 14 | sqlite-web in main requirements | Low | 2026-02-16 | Saul P |
| 16 | Inefficient note count query (len vs count) | Low | 2026-02-16 | Saul P |
| 17 | Legacy Model.query API usage | Low | 2026-02-16 | Saul P |
| 18 | No rate limiting on login endpoint | High | 2026-02-24 | Saul P |
| 19 | Cookie security settings not configured | Medium | 2026-02-24 | Saul P |
| 20 | No email normalization (case-insensitive lookup) | Medium | 2026-02-24 | Saul P |
| 21 | Hardcoded SQLALCHEMY_DATABASE_URI | Medium | 2026-02-24 | Saul P |
| 22 | CDN resources loaded without SRI | Medium | 2026-02-24 | Saul P |
| 23 | run.py binds to 0.0.0.0 with debug enabled | Low-Medium | 2026-02-24 | Saul P |
| 24 | Dead service methods (delete_user, get_all_users) | Low | 2026-02-24 | Saul P |
| 25 | load_user integer conversion not guarded | Low | 2026-02-24 | Saul P |
| 26 | Orphan templates (users/list.html, users/new.html) | Low | 2026-02-24 | Saul P |
| 27 | No custom error handlers (403/404/500) | Low | 2026-02-24 | Saul P |
| 28 | Email existence checked before format validation | Low | 2026-02-24 | Saul P |
| 29 | LoginManager missing login_message_category | Low | 2026-02-24 | Saul P |
| 30 | unshare_note does not clear share_token | Low | 2026-02-24 | Saul P |
