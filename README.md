# CorpCorp Employee Portal — CTF Lab

A deliberately vulnerable web application for SQL injection practice.  
**Do not deploy on a public-facing server.**

---

## Stack

| Component | Tech |
|-----------|------|
| Backend   | Python / Flask |
| Database  | MySQL 8.0 |
| Container | Docker + docker-compose |

---

## Setup

### Prerequisites
- Docker Desktop (or Docker Engine + docker-compose)
- Git

### Run

```bash
git clone CropCrop-ctf
cd sqli-lab
docker-compose up --build
```

App will be available at **http://localhost:5000**

To stop:
```bash
docker-compose down -v   # -v removes the DB volume too (clean reset)
```

---

## For the Red Team — Attack Surface

The application has **two intentional vulnerabilities** in the login endpoint:

1. **Login Bypass** — The authentication query is constructed via string concatenation.  
   Think about what happens when you control the `username` or `password` field directly inside a SQL `WHERE` clause.

2. **Error-Based Information Disclosure** — The application surfaces raw database error messages in the browser response.  
   Malformed queries can leak schema details, table names, and data types.

### Hints (read only if stuck)

<details>
<summary>Hint 1 — Login bypass</summary>

Try submitting a username that makes the WHERE clause always evaluate to true.  
Classic: `' OR '1'='1' -- `

</details>

<details>
<summary>Hint 2 — Error-based extraction</summary>

Inject syntax that causes a MySQL error containing data — look into `extractvalue()` or `updatexml()` functions. The error message will be rendered on the page.

</details>

---

## Database Schema (for defenders / blue team)

```sql
TABLE users          -- id, username, password (plaintext!), role, email, department
TABLE employee_records  -- user_id, salary, ssn, notes
```

Seed accounts:

| Username  | Password      | Role     |
|-----------|---------------|----------|
| admin     | sup3rs3cr3t!  | admin    |
| jsmith    | password123   | employee |
| mwilson   | qwerty99      | employee |
| tgraves   | letmein       | manager  |

---

## For the Blue Team — Fix Checklist

When it's your turn to patch:

- [ ] Replace string-concatenated queries with **parameterized queries** (`cursor.execute(query, (user, pw))`)
- [ ] Catch DB exceptions and return a **generic error message** — never expose `str(e)`
- [ ] Hash passwords (bcrypt / argon2) — plaintext storage is its own vulnerability
- [ ] Add rate limiting / lockout on `/login`
- [ ] Remove the debug comment block from the template

---

## Project Structure

```
sqli-lab/
├── app/
│   ├── app.py               ← Flask app (vulnerabilities live here)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── mysql-init/
│   └── init.sql             ← DB schema + seed data
├── docker-compose.yml
└── README.md
```
