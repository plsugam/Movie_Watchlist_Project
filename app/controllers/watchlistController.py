from flask import render_template, request, redirect, url_for, session, flash
from app.database import get_connection
from app.repository import watchlist_repo

VALID_TYPES = {"movie", "series", "anime"}
VALID_STATUSES = {"plan", "watching", "completed", "dropped"}


def dashboard():
    user_id = session["user_id"]

    total = watchlist_repo.get_count_by_user(user_id)
    status_counts = watchlist_repo.get_status_counts(user_id)
    type_counts = watchlist_repo.get_type_counts(user_id)
    recent = watchlist_repo.get_recent(user_id)

    return render_template(
        "dashboard.html",
        total=total,
        status_counts=status_counts,
        type_counts=type_counts,
        recent=recent,
    )


def view_watchlist():
    user_id = session["user_id"]

    search = request.args.get("search", "").strip()
    filter_type = request.args.get("type", "")
    filter_status = request.args.get("status", "")
    sort = request.args.get("sort", "newest")

    query = "SELECT * FROM watchlist WHERE user_id = %s"
    params = [user_id]

    if search:
        query += " AND title LIKE %s"
        params.append(f"%{search}%")
    if filter_type and filter_type in VALID_TYPES:
        query += " AND type = %s"
        params.append(filter_type)
    if filter_status and filter_status in VALID_STATUSES:
        query += " AND status = %s"
        params.append(filter_status)

    if sort == "oldest":
        query += " ORDER BY created_at ASC"
    elif sort == "title":
        query += " ORDER BY title ASC"
    elif sort == "rating":
        query += " ORDER BY rating DESC"
    else:
        query += " ORDER BY created_at DESC"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    titles = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "watchlist.html",
        titles=titles,
        search=search,
        filter_type=filter_type,
        filter_status=filter_status,
        sort=sort,
    )


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
    entry = watchlist_repo.get_by_id(id, user_id)

    if not entry:
        flash("Title not found.", "danger")
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
            return render_template("edit.html", entry=entry)
        if len(title) > 200:
            flash("Title must be under 200 characters.", "danger")
            return render_template("edit.html", entry=entry)
        if type_ not in VALID_TYPES:
            flash("Invalid type selected.", "danger")
            return render_template("edit.html", entry=entry)
        if status not in VALID_STATUSES:
            flash("Invalid status selected.", "danger")
            return render_template("edit.html", entry=entry)
        if year:
            try:
                year = int(year)
                if year < 1900 or year > 2030:
                    raise ValueError
            except ValueError:
                flash("Please enter a valid year between 1900 and 2030.", "danger")
                return render_template("edit.html", entry=entry)
        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                flash("Rating must be between 1 and 5.", "danger")
                return render_template("edit.html", entry=entry)

        conn = get_connection()
        cursor = conn.cursor()
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
