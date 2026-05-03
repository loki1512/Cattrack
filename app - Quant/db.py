import sqlite3
from datetime import date, timedelta, datetime

DB = "catmath.db"

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = conn()
    cur = c.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS user_stats (
        id INTEGER PRIMARY KEY,
        streak INTEGER DEFAULT 0,
        last_practice TEXT,
        total_session_seconds INTEGER DEFAULT 0,
        total_questions_answered INTEGER DEFAULT 0,
        total_correct INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS best_times (
        lesson_id TEXT PRIMARY KEY,
        best_time_seconds INTEGER,
        best_score INTEGER,
        achieved_on TEXT
    );

    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id TEXT,
        lesson_name TEXT,
        date TEXT,
        score INTEGER,
        total INTEGER,
        time_seconds INTEGER,
        accuracy INTEGER
    );

    CREATE TABLE IF NOT EXISTS session_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        seconds INTEGER
    );

    -- PYQ Tables for Percentages
    CREATE TABLE IF NOT EXISTS pyq_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        date TEXT NOT NULL,
        score INTEGER,
        total INTEGER,
        time_seconds INTEGER,
        accuracy INTEGER,
        level TEXT DEFAULT 'medium'
    );

    CREATE TABLE IF NOT EXISTS pyq_best_times (
        topic TEXT PRIMARY KEY,
        best_time_seconds INTEGER,
        best_score INTEGER,
        best_accuracy INTEGER,
        achieved_on TEXT
    );

    CREATE TABLE IF NOT EXISTS pyq_user_stats (
        id INTEGER PRIMARY KEY,
        current_streak INTEGER DEFAULT 0,
        best_streak INTEGER DEFAULT 0,
        last_practice_date TEXT,
        total_sessions_completed INTEGER DEFAULT 0,
        total_questions_answered INTEGER DEFAULT 0,
        total_correct INTEGER DEFAULT 0
    );
    """)
    cur.execute("INSERT OR IGNORE INTO user_stats (id) VALUES (1)")
    cur.execute("INSERT OR IGNORE INTO pyq_user_stats (id) VALUES (1)")
    c.commit()
    c.close()

def get_stats():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM user_stats WHERE id=1")
    stats = dict(cur.fetchone())
    cur.execute("SELECT * FROM best_times")
    best_times = {r["lesson_id"]: dict(r) for r in cur.fetchall()}
    cur.execute("SELECT * FROM history ORDER BY id DESC LIMIT 20")
    history = [dict(r) for r in cur.fetchall()]
    c.close()
    return {"stats": stats, "best_times": best_times, "history": history}

def update_streak():
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT streak, last_practice FROM user_stats WHERE id=1")
    row = cur.fetchone()
    today = date.today()
    streak = row["streak"] or 0
    last = date.fromisoformat(row["last_practice"]) if row["last_practice"] else None

    if last == today:
        pass
    elif last == today - timedelta(days=1):
        streak += 1
    else:
        streak = 1

    cur.execute("UPDATE user_stats SET streak=?, last_practice=? WHERE id=1", (streak, str(today)))
    c.commit()
    c.close()
    return streak

def save_result(lesson_id, lesson_name, score, total, time_seconds):
    c = conn()
    cur = c.cursor()
    accuracy = int(score / total * 100) if total else 0

    cur.execute("""INSERT INTO history (lesson_id, lesson_name, date, score, total, time_seconds, accuracy)
                   VALUES (?,?,DATE('now'),?,?,?,?)""",
                (lesson_id, lesson_name, score, total, time_seconds, accuracy))

    # update best time
    cur.execute("SELECT best_time_seconds, best_score FROM best_times WHERE lesson_id=?", (lesson_id,))
    existing = cur.fetchone()
    if not existing or time_seconds < existing["best_time_seconds"] or (time_seconds == existing["best_time_seconds"] and score > existing["best_score"]):
        cur.execute("""INSERT INTO best_times (lesson_id, best_time_seconds, best_score, achieved_on)
                       VALUES (?,?,?,DATE('now'))
                       ON CONFLICT(lesson_id) DO UPDATE SET
                       best_time_seconds=excluded.best_time_seconds,
                       best_score=excluded.best_score,
                       achieved_on=excluded.achieved_on""",
                    (lesson_id, time_seconds, score))

    # update aggregate stats
    cur.execute("""UPDATE user_stats SET
                   total_questions_answered = total_questions_answered + ?,
                   total_correct = total_correct + ?
                   WHERE id=1""", (total, score))
    c.commit()
    c.close()

def log_session_time(seconds):
    if seconds < 5:
        return
    c = conn()
    cur = c.cursor()
    cur.execute("INSERT INTO session_log (date, seconds) VALUES (DATE('now'), ?)", (seconds,))
    cur.execute("UPDATE user_stats SET total_session_seconds = total_session_seconds + ? WHERE id=1", (seconds,))
    c.commit()
    c.close()

def fmt_time(s):
    if s is None:
        return "—"
    m, sec = divmod(int(s), 60)
    return f"{m}m {sec:02d}s" if m else f"{sec}s"

def fmt_hms(s):
    s = int(s or 0)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h {m}m"
    elif m:
        return f"{m}m {sec}s"
    return f"{sec}s"

# ── PYQ Functions ────────────────────────────────────────────────────────────

def get_pyq_stats():
    """Get PYQ user stats."""
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT * FROM pyq_user_stats WHERE id=1")
    row = cur.fetchone()
    stats = dict(row) if row else {}
    
    # Get best times for percentages
    cur.execute("SELECT * FROM pyq_best_times WHERE topic='percentages'")
    best = cur.fetchone()
    best_times = dict(best) if best else {}
    
    # Get recent sessions
    cur.execute("SELECT * FROM pyq_sessions ORDER BY id DESC LIMIT 20")
    sessions = [dict(r) for r in cur.fetchall()]
    
    c.close()
    return {"stats": stats, "best_times": best_times, "sessions": sessions}

def update_pyq_streak():
    """Update PYQ streak and return current streak."""
    c = conn()
    cur = c.cursor()
    today = date.today()
    
    cur.execute("SELECT current_streak, best_streak, last_practice_date FROM pyq_user_stats WHERE id=1")
    row = cur.fetchone()
    current = row["current_streak"] or 0
    best = row["best_streak"] or 0
    last = date.fromisoformat(row["last_practice_date"]) if row["last_practice_date"] else None
    
    if last != today:
        if last == today - timedelta(days=1):
            current += 1
        else:
            current = 1
        
        if current > best:
            best = current
        
        cur.execute("UPDATE pyq_user_stats SET current_streak=?, best_streak=?, last_practice_date=? WHERE id=1",
                    (current, best, str(today)))
        c.commit()
    
    c.close()
    return current

def save_pyq_result(topic, score, total, time_seconds, level="medium"):
    """Save a PYQ session result."""
    c = conn()
    cur = c.cursor()
    accuracy = int(score / total * 100) if total else 0
    
    cur.execute("""INSERT INTO pyq_sessions (topic, date, score, total, time_seconds, accuracy, level)
                   VALUES (?,DATE('now'),?,?,?,?,?)""",
                (topic, score, total, time_seconds, accuracy, level))
    
    # Update best time for topic
    cur.execute("SELECT best_time_seconds, best_score, best_accuracy FROM pyq_best_times WHERE topic=?", (topic,))
    existing = cur.fetchone()
    
    if not existing:
        cur.execute("""INSERT INTO pyq_best_times (topic, best_time_seconds, best_score, best_accuracy, achieved_on)
                       VALUES (?,?,?,?,DATE('now'))""",
                    (topic, time_seconds, score, accuracy))
    else:
        # Update if better time or same time with better score
        if time_seconds < existing["best_time_seconds"] or \
           (time_seconds == existing["best_time_seconds"] and score > existing["best_score"]):
            cur.execute("""UPDATE pyq_best_times SET best_time_seconds=?, best_score=?, best_accuracy=?, achieved_on=DATE('now')
                           WHERE topic=?""", (time_seconds, score, accuracy))
    
    # Update aggregate stats
    cur.execute("""UPDATE pyq_user_stats SET
                   total_sessions_completed = total_sessions_completed + 1,
                   total_questions_answered = total_questions_answered + ?,
                   total_correct = total_correct + ?
                   WHERE id=1""", (total, score))
    
    c.commit()
    c.close()