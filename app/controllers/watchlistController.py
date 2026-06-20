from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection


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

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO watchlist (user_id, title, type, status, genre, year, rating, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                title,
                type_,
                status,
                genre or None,
                year or None,
                rating or None,
                notes or None,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Title added to your watchlist!", "success")
        return redirect(url_for("watchlist.view_watchlist"))

    return render_template("add.html")
