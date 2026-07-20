from app.database import get_connection


def get_all_by_user(user_id):
    """Fetch all watchlist entries for a user ordered by newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM watchlist WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_by_id(entry_id, user_id):
    """Fetch a single watchlist entry by ID, scoped to the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM watchlist WHERE id = %s AND user_id = %s",
        (entry_id, user_id)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def get_count_by_user(user_id):
    """Get total number of titles in a user's watchlist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) as total FROM watchlist WHERE user_id = %s",
        (user_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result["total"]


def get_status_counts(user_id):
    """Get count of entries grouped by status for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM watchlist WHERE user_id = %s
        GROUP BY status
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row["status"]: row["count"] for row in rows}


def get_type_counts(user_id):
    """Get count of entries grouped by type for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, COUNT(*) as count
        FROM watchlist WHERE user_id = %s
        GROUP BY type
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {row["type"]: row["count"] for row in rows}


def get_recent(user_id, limit=5):
    """Get the most recently added titles for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM watchlist WHERE user_id = %s
        ORDER BY created_at DESC LIMIT %s
    """, (user_id, limit))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
