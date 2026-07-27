from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_connection
import re


def home():
    return redirect(url_for("watchlist.dashboard"))


def _validate_password(password):
    """Returns error message if invalid, empty string if valid."""
    password = password.strip()
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return ""


def login():
    if session.get("user_id"):
        return redirect(url_for("watchlist.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("login.html")
        if len(email) > 150:
            flash("Invalid email address.", "danger")
            return render_template("login.html")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]
            flash("Login successful!", "success")
            if user["role"] == "admin":
                return redirect(url_for("auth.admin_panel"))
            return redirect(url_for("watchlist.dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")


def register():
    if session.get("user_id"):
        return redirect(url_for("watchlist.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")
        if len(name) > 100:
            flash("Name must be under 100 characters.", "danger")
            return render_template("register.html")
        if len(email) > 150:
            flash("Email must be under 150 characters.", "danger")
            return render_template("register.html")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Please enter a valid email address.", "danger")
            return render_template("register.html")

        pwd_error = _validate_password(password)
        if pwd_error:
            flash(pwd_error, "danger")
            return render_template("register.html")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("Email already exists.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))


def admin_panel():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id")
    users = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM watchlist")
    total_titles = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()["total"]

    cursor.close()
    conn.close()
    return render_template("admin.html", users=users,
                           total_titles=total_titles,
                           total_users=total_users)


def admin_delete_user(id):
    if id == session.get("user_id"):
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("auth.admin_panel"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("User deleted successfully.", "success")
    return redirect(url_for("auth.admin_panel"))
