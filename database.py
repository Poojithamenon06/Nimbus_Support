"""
Thin SQLite layer. No ORM on purpose, it's easier to explain line-by-line
in a demo/interview than an ORM would be.
"""
import sqlite3
import os
from datetime import datetime
from data.kb_seed import KB_ARTICLES

DB_PATH = os.path.join(os.path.dirname(__file__), "nimbus.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(reset=False):
    """Create tables and seed the knowledge base if empty."""
    if reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kb_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            keywords TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            priority TEXT NOT NULL DEFAULT 'Normal',
            escalated INTEGER NOT NULL DEFAULT 0,
            escalation_reason TEXT,
            answer TEXT,
            matched_article_id INTEGER,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()

    # seed KB only if empty, so re-running the app doesn't duplicate rows
    cur.execute("SELECT COUNT(*) as c FROM kb_articles")
    if cur.fetchone()["c"] == 0:
        for a in KB_ARTICLES:
            cur.execute(
                "INSERT INTO kb_articles (category, title, content, keywords) VALUES (?, ?, ?, ?)",
                (a["category"], a["title"], a["content"], a["keywords"]),
            )
        conn.commit()

    conn.close()


def list_kb_articles():
    conn = get_db()
    rows = conn.execute("SELECT * FROM kb_articles ORDER BY category, title").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_kb_article(category, title, content, keywords=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO kb_articles (category, title, content, keywords) VALUES (?, ?, ?, ?)",
        (category, title, content, keywords),
    )
    conn.commit()
    conn.close()


def delete_kb_article(article_id):
    conn = get_db()
    conn.execute("DELETE FROM kb_articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()


def create_ticket(title, message, category, confidence, escalated, escalation_reason, answer, matched_article_id, priority="Normal"):
    conn = get_db()
    cur = conn.execute(
        """INSERT INTO tickets
           (title, message, category, confidence, status, priority, escalated, escalation_reason, answer, matched_article_id, created_at)
           VALUES (?, ?, ?, ?, 'open', ?, ?, ?, ?, ?, ?)""",
        (title, message, category, confidence, priority, int(escalated), escalation_reason, answer, matched_article_id,
         datetime.utcnow().isoformat()),
    )
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    return ticket_id


def list_tickets():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_escalations():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tickets WHERE escalated = 1 ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ticket(ticket_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def resolve_ticket(ticket_id):
    conn = get_db()
    conn.execute("UPDATE tickets SET status = 'resolved' WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()


def dashboard_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) c FROM tickets").fetchone()["c"]
    escalated = conn.execute("SELECT COUNT(*) c FROM tickets WHERE escalated = 1").fetchone()["c"]
    resolved = conn.execute("SELECT COUNT(*) c FROM tickets WHERE status = 'resolved'").fetchone()["c"]
    avg_conf_row = conn.execute("SELECT AVG(confidence) a FROM tickets").fetchone()
    avg_conf = round((avg_conf_row["a"] or 0) * 100)
    by_category = conn.execute(
        "SELECT category, COUNT(*) c FROM tickets GROUP BY category"
    ).fetchall()
    recent = conn.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()
    return {
        "total": total,
        "escalated": escalated,
        "resolved": resolved,
        "escalation_rate": round((escalated / total) * 100) if total else 0,
        "resolution_rate": round((resolved / total) * 100) if total else 0,
        "avg_confidence": avg_conf,
        "by_category": {r["category"]: r["c"] for r in by_category},
        "recent": [dict(r) for r in recent],
    }
