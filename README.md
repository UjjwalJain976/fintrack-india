# FinTrack India

FinTrack India is a personal finance tracker for young Indian professionals. The app stores records in Supabase PostgreSQL through Flask-SQLAlchemy.

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Supabase PostgreSQL
- Jinja2 templates
- HTML, CSS, JavaScript
- python-dotenv
- psycopg2-binary
- gunicorn

## Database

The app uses Supabase PostgreSQL through `DATABASE_URL` in a local `.env` file. SQLite and CSV are not used for active storage.

Expected Supabase tables:

- `income`
- `expenses`
- `fd_accounts`
- `sip_investments`
- `goals`

## Run Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install requirements:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```powershell
Copy-Item .env.example .env
```

Paste your Supabase PostgreSQL connection string into `DATABASE_URL`:

```env
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://postgres.xxxxx:YOUR_PASSWORD@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

Do not commit `.env`, database passwords, Supabase keys, or other secrets.

Run locally:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Features Completed

- Dashboard with income, expenses, savings, investments, goals, and financial health score
- Month-wise financial dashboard with charts and recent transactions
- Income tracker with add, list, and delete
- Expense tracker with add, list, category, payment mode, and delete
- FD tracker with add, list, and delete
- SIP tracker with add, list, and delete
- Goals tracker with add, list, and delete
- Supabase PostgreSQL persistence

## Render Deployment

The app is deployed on Render and uses Supabase PostgreSQL for persistent storage.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn wsgi:app
```

## Future Plan

Later, add login, user-specific records, and deployment configuration after the core Supabase workflows are stable.
