from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection

VALID_TYPES = {"movie", "series", "anime"}
VALID_STATUSES = {"plan", "watching", "completed", "dropped"}


def dashboard():
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM watchlist WHERE user_id = %s", (user_id,))
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM watchlist WHERE user_id = %s
        GROUP BY status
    """, (user_id,))
    status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM watchlist WHERE user_id = %s
        GROUP BY type
    """, (user_id,))
    type_counts = {row["type"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT * FROM watchlist WHERE user_id = %s
        ORDER BY created_at DESC LIMIT 5
    """, (user_id,))
    recent = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total=total,
        status_counts=status_counts,
        type_counts=type_counts,
        recent=recent,
    )


def view_watchlist():
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM watchlist WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    titles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("watchlist.html", titles=titles)


def add_title():
    if request.method == "POST":
        user_id = session["user_id"]
        title = request.form.get("title", "").strip()
        type_ = request.form.get("type", "").strip()
        status = request.form.get("status", "plan").strip()
        genre = request.form.get("genre", "").strip()
        year = request.form.get("year", "").strip()
        rating = request.form.get("rating", "").strip()
        notes = request.form.get("notes", "").strip()

        if not title or not type_:
            flash("Title and type are required.", "danger")
            return render_template("add.html")
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("add.html")
        if type_ not in VALID_TYPES:
            flash("Invalid type selected.", "danger")
            return render_template("add.html")
        if status not in VALID_STATUSES:
            flash("Invalid status selected.", "danger")
            return render_template("add.html")
        if genre and len(genre) > 50:
            flash("Genre must be under 50 characters.", "danger")
            return render_template("add.html")
        if year:
            try:
                year = int(year)
                if year < 1900 or year > 2030:
                    raise ValueError
            except ValueError:
                flash("Please enter a valid year between 1900 and 2030.", "danger")
                return render_template("add.html")
        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                flash("Rating must be a number between 1 and 5.", "danger")
                return render_template("add.html")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO watchlist (user_id, title, type, status, genre, year, rating, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id, title, type_, status,
                genre or None, year or None, rating or None, notes or None,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Title added to your watchlist!", "success")
        return redirect(url_for("watchlist.view_watchlist"))

    return render_template("add.html")


def edit_title(id):
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM watchlist WHERE id = %s AND user_id = %s",
        (id, user_id)
    )
    entry = cursor.fetchone()

    if not entry:
        flash("Title not found.", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for("watchlist.view_watchlist"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        type_ = request.form.get("type", "").strip()
        status = request.form.get("status", "plan").strip()
        genre = request.form.get("genre", "").strip()
        year = request.form.get("year", "").strip()
        rating = request.form.get("rating", "").strip()
        notes = request.form.get("notes", "").strip()

        if not title or not type_:
            flash("Title and type are required.", "danger")
            cursor.close()
            conn.close()
            return render_template("edit.html", entry=entry)
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            cursor.close()
            conn.close()
            return render_template("edit.html", entry=entry)
        if type_ not in VALID_TYPES:
            flash("Invalid type selected.", "danger")
            cursor.close()
            conn.close()
            return render_template("edit.html", entry=entry)
        if status not in VALID_STATUSES:
            flash("Invalid status selected.", "danger")
            cursor.close()
            conn.close()
            return render_template("edit.html", entry=entry)
        if year:
            try:
                year = int(year)
                if year < 1900 or year > 2030:
                    raise ValueError
            except ValueError:
                flash("Please enter a valid year between 1900 and 2030.", "danger")
                cursor.close()
                conn.close()
                return render_template("edit.html", entry=entry)
        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                flash("Rating must be a number between 1 and 5.", "danger")
                cursor.close()
                conn.close()
                return render_template("edit.html", entry=entry)

        cursor.execute(
            """
            UPDATE watchlist
            SET title=%s, type=%s, status=%s, genre=%s, year=%s, rating=%s, notes=%s
            WHERE id=%s AND user_id=%s
            """,
            (
                title, type_, status,
                genre or None, year or None, rating or None, notes or None,
                id, user_id,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Title updated successfully!", "success")
        return redirect(url_for("watchlist.view_watchlist"))

    cursor.close()
    conn.close()
    return render_template("edit.html", entry=entry)


def delete_title(id):
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM watchlist WHERE id = %s AND user_id = %s",
        (id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Title removed from your watchlist.", "success")
    return redirect(url_for("watchlist.view_watchlist"))
