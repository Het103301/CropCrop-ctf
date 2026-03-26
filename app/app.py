from flask import Flask, request, render_template, session, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "changeme_insecure_key_123"

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "user": os.environ.get("DB_USER", "webapp"),
    "password": os.environ.get("DB_PASS", "webapp_pass"),
    "database": os.environ.get("DB_NAME", "corp_portal"),
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    debug_info = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)

            # VULNERABILITY 1: String-concatenated query — login bypass via ' OR '1'='1
            query = (
                "SELECT * FROM users WHERE username = '"
                + username
                + "' AND password = '"
                + password
                + "'"
            )

            # VULNERABILITY 2: Error-based — raw DB errors exposed to client
            cursor.execute(query)
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session["user"] = user["username"]
                session["role"] = user["role"]
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid credentials. Please try again."

        except mysql.connector.Error as e:
            # VULNERABILITY 2 continued: full DB error message shown in response
            debug_info = f"Database error: {str(e)}"
            error = "An error occurred. See details below."

    return render_template("login.html", error=error, debug_info=debug_info)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["user"], role=session["role"])


@app.route("/employees")
def employees():
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT users.id, users.username, users.email, users.department, users.role "
        "FROM users ORDER BY users.id"
    )
    staff = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("employees.html", staff=staff)


@app.route("/employees/<int:uid>")
def employee_detail(uid):
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return redirect(url_for("dashboard"))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT users.username, users.email, users.department, users.role, "
        "employee_records.salary, employee_records.ssn, employee_records.notes, employee_records.message "
        "FROM users JOIN employee_records ON employee_records.user_id = users.id "
        "WHERE users.id = %s",
        (uid,)
    )
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if not record:
        return redirect(url_for("employees"))
    return render_template("employee_detail.html", record=record)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
