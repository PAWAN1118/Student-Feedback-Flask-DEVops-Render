import sqlite3
import os
import csv
import io
from datetime import datetime


def _connect(db_path: str) -> sqlite3.Connection:
    if db_path != ':memory:':
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    conn = _connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL,
            course       TEXT,
            rating       TEXT,
            message      TEXT    NOT NULL,
            submitted_at TEXT    DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    conn.close()


def add_feedback(db_path, name, course, rating, message):
    conn = _connect(db_path)
    conn.execute(
        'INSERT INTO feedback (name, course, rating, message, submitted_at) VALUES (?,?,?,?,?)',
        (name, course, rating, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    conn.commit()
    conn.close()


def get_paginated_feedback(db_path, page, per_page):
    conn   = _connect(db_path)
    total  = conn.execute('SELECT COUNT(*) FROM feedback').fetchone()[0]
    offset = (page - 1) * per_page
    rows   = conn.execute(
        'SELECT * FROM feedback ORDER BY submitted_at DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows], total


def get_all_feedback(db_path):
    conn = _connect(db_path)
    rows = conn.execute('SELECT * FROM feedback ORDER BY submitted_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_feedback_by_id(db_path, feedback_id):
    conn = _connect(db_path)
    row  = conn.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_feedback(db_path, feedback_id, name, course, rating, message):
    conn = _connect(db_path)
    conn.execute(
        'UPDATE feedback SET name=?, course=?, rating=?, message=? WHERE id=?',
        (name, course, rating, message, feedback_id)
    )
    conn.commit()
    conn.close()


def delete_feedback(db_path, feedback_id):
    conn = _connect(db_path)
    conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()


def search_feedback(db_path, query):
    conn = _connect(db_path)
    q    = f'%{query}%'
    rows = conn.execute(
        'SELECT * FROM feedback WHERE name LIKE ? OR course LIKE ? OR message LIKE ? ORDER BY submitted_at DESC',
        (q, q, q)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_stats(db_path):
    conn   = _connect(db_path)
    total  = conn.execute('SELECT COUNT(*) FROM feedback').fetchone()[0]
    avg    = conn.execute(
        "SELECT ROUND(AVG(CAST(rating AS REAL)),1) FROM feedback WHERE rating != '' AND rating IS NOT NULL"
    ).fetchone()[0]
    dist   = conn.execute(
        "SELECT rating, COUNT(*) as count FROM feedback WHERE rating != '' AND rating IS NOT NULL GROUP BY rating ORDER BY rating"
    ).fetchall()
    recent = conn.execute(
        "SELECT COUNT(*) FROM feedback WHERE submitted_at >= datetime('now', '-7 days')"
    ).fetchone()[0]
    conn.close()
    return {'total': total, 'avg_rating': avg or 0, 'distribution': [dict(r) for r in dist], 'recent': recent}


def export_csv(db_path):
    rows   = get_all_feedback(db_path)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['id','name','course','rating','message','submitted_at'])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def reset_db(db_path):
    conn = _connect(db_path)
    conn.execute('DROP TABLE IF EXISTS feedback')
    conn.commit()
    conn.close()
    init_db(db_path)
