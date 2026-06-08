# AGENTS.md

## Project

FinTrack India is a Flask application using Supabase PostgreSQL through Flask-SQLAlchemy.

## Rules

- Use Supabase PostgreSQL through `DATABASE_URL`.
- Do not use SQLite.
- Do not use CSV files for active storage.
- Use Flask-SQLAlchemy for database access.
- Do not hardcode database passwords, Supabase API keys, or other secrets.
- Use environment variables for secrets and database configuration.
- Do not edit live Render code directly.
- Keep changes focused on the local project files.

## Run Commands

- Local: `python app.py`
- Production: `gunicorn app:app`
