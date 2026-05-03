from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from db import init_db, get_stats, update_streak, save_result, log_session_time, fmt_time, fmt_hms
from db import get_pyq_stats, update_pyq_streak, save_pyq_result
from questions import (
    LESSONS, LESSON_MAP, CATEGORY_ORDER, CATEGORY_LABELS, CATEGORY_ICONS,
    generate_quiz, is_unlocked, check_answer, generate_pyq_quiz
)

app = Flask(__name__)
app.secret_key = "catmath_no_auth_2024"

@app.before_request
def setup():
    init_db()

# ── helpers ──────────────────────────────────────────────────────────────────
def get_completed(best_times):
    """Lessons where user scored >= 15/20 (75%) are considered 'completed' for unlock."""
    return {lid for lid, bt in best_times.items() if bt.get("best_score", 0) >= 15}

# ── routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    data = get_stats()
    stats = data["stats"]
    best_times = data["best_times"]
    history = data["history"]
    completed = get_completed(best_times)

    categories = {}
    for cat in CATEGORY_ORDER:
        cat_lessons = [l for l in LESSONS if l["category"] == cat]
        for lesson in cat_lessons:
            lid = lesson["id"]
            lesson["unlocked"] = is_unlocked(lid, completed)
            lesson["best"] = best_times.get(lid)
            lesson["done"] = lid in completed
        categories[cat] = {
            "label": CATEGORY_LABELS[cat],
            "icon": CATEGORY_ICONS[cat],
            "lessons": cat_lessons
        }

    return render_template("home.html",
        stats=stats, categories=categories,
        history=history[:10], fmt_time=fmt_time, fmt_hms=fmt_hms)

@app.route("/lesson/<lesson_id>")
def lesson(lesson_id):
    data = get_stats()
    completed = get_completed(data["best_times"])
    if not is_unlocked(lesson_id, completed):
        return redirect(url_for("home"))

    l = LESSON_MAP.get(lesson_id)
    if not l:
        return redirect(url_for("home"))

    quiz = generate_quiz(lesson_id, count=20)
    session["quiz"] = quiz
    session["lesson_id"] = lesson_id
    session["lesson_name"] = l["name"]
    best = data["best_times"].get(lesson_id)
    return render_template("quiz.html",
        lesson=l, quiz=quiz, best=best, fmt_time=fmt_time)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    quiz = session.get("quiz", [])
    lesson_id = session.get("lesson_id", "unknown")
    lesson_name = session.get("lesson_name", "Lesson")
    time_seconds = int(data.get("time_seconds", 0))
    answers = data.get("answers", [])

    results = []
    score = 0
    for i, q in enumerate(quiz):
        user_ans = answers[i] if i < len(answers) else ""
        correct = check_answer(user_ans, q["a"])
        if correct:
            score += 1
        results.append({
            "q": q["q"], "correct_a": q["a"],
            "user_a": user_ans, "ok": correct,
            "hint": q.get("hint", "")
        })

    save_result(lesson_id, lesson_name, score, len(quiz), time_seconds)
    streak = update_streak()
    log_session_time(time_seconds)

    session["last_result"] = {
        "lesson_id": lesson_id, "lesson_name": lesson_name,
        "score": score, "total": len(quiz),
        "time_seconds": time_seconds, "streak": streak,
        "results": results
    }
    return jsonify({"redirect": url_for("result")})

@app.route("/result")
def result():
    r = session.get("last_result")
    if not r:
        return redirect(url_for("home"))
    data = get_stats()
    best = data["best_times"].get(r["lesson_id"])
    return render_template("result.html", r=r, best=best, fmt_time=fmt_time)

@app.route("/log_time", methods=["POST"])
def log_time():
    seconds = request.get_json().get("seconds", 0)
    log_session_time(seconds)
    return jsonify({"ok": True})

# ── PYQ Routes ───────────────────────────────────────────────────────────────

@app.route("/pyqs")
def pyqs():
    """PYQ main page - shows topic selection and stats."""
    data = get_pyq_stats()
    stats = data["stats"]
    best_times = data["best_times"]
    sessions = data["sessions"]
    
    topics = [
        {
            "id": "percentages",
            "name": "Percentages",
            "icon": "%",
            "description": "CAT PYQs on percentages, mixtures, ratios",
            "best": best_times.get("percentages", {})
        }
    ]
    
    return render_template("pyqs.html",
        stats=stats, topics=topics, sessions=sessions,
        fmt_time=fmt_time, fmt_hms=fmt_hms)

@app.route("/pyq/<topic>")
def pyq_quiz(topic):
    """Start a PYQ quiz session."""
    if topic != "percentages":
        return redirect(url_for("pyqs"))
    
    data = get_pyq_stats()
    best = data["best_times"].get(topic, {})
    
    quiz = generate_pyq_quiz(topic, count=10)
    session["pyq_quiz"] = quiz
    session["pyq_topic"] = topic
    session["pyq_topic_name"] = "Percentages"
    session["pyq_best"] = best
    
    return render_template("pyq_quiz.html",
        topic=topic, topic_name="Percentages",
        quiz=quiz, best=best, fmt_time=fmt_time)

@app.route("/pyq_submit", methods=["POST"])
def pyq_submit():
    """Submit PYQ quiz and save results."""
    data = request.get_json()
    quiz = session.get("pyq_quiz", [])
    topic = session.get("pyq_topic", "unknown")
    topic_name = session.get("pyq_topic_name", "PYQ")
    time_seconds = int(data.get("time_seconds", 0))
    answers = data.get("answers", [])
    
    results = []
    score = 0
    for i, q in enumerate(quiz):
        user_ans = answers[i] if i < len(answers) else ""
        correct = check_answer(user_ans, q["a"])
        if correct:
            score += 1
        results.append({
            "q": q["q"], "correct_a": q["a"],
            "user_a": user_ans, "ok": correct,
            "hint": q.get("hint", ""),
            "level": q.get("level", "medium")
        })
    
    # Determine level based on score
    if score >= 8:
        level = "easy"
    elif score >= 5:
        level = "medium"
    else:
        level = "hard"
    
    save_pyq_result(topic, score, len(quiz), time_seconds, level)
    pyq_streak = update_pyq_streak()
    accuracy = int(score / len(quiz) * 100) if len(quiz) else 0
    
    session["pyq_last_result"] = {
        "topic": topic, "topic_name": topic_name,
        "score": score, "total": len(quiz),
        "time_seconds": time_seconds, "streak": pyq_streak,
        "level": level, "accuracy": accuracy, "results": results
    }
    return jsonify({"redirect": url_for("pyq_result")})

@app.route("/pyq_result")
def pyq_result():
    """Show PYQ quiz results."""
    r = session.get("pyq_last_result")
    if not r:
        return redirect(url_for("pyqs"))
    
    data = get_pyq_stats()
    best = data["best_times"].get(r["topic"], {})
    
    return render_template("pyq_result.html", r=r, best=best, fmt_time=fmt_time)

@app.route("/pyq_log_time", methods=["POST"])
def pyq_log_time():
    """Log time for PYQ session."""
    seconds = request.get_json().get("seconds", 0)
    log_session_time(seconds)
    return jsonify({"ok": True})

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)