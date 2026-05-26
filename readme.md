# CAT Math Trainer 🧮

A focused CAT math speed trainer for practicing core mental-math skills.

## Setup & Run

```bash
cd "c:\CATRACK\app - Quant"
pip install -r requirements.txt
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## What this app includes

### Core learning categories
| Category | Content |
|---|---|
| **Multiplication Tables** | 1–10, 11–20, 21–30, mixed drills, cross-multiply practice |
| **Squares & Square Roots** | Squares 1–50, reverse root recall |
| **Cubes** | Cubes 1–20 and mixed recall |
| **Percentages & Fractions** | Fraction → percent, percent → fraction, percentage-of-number |
| **Arithmetic Speed** | 2-digit / 3-digit addition and subtraction, mixed arithmetic drills, CAT-style speed drill |

### Feature highlights
- ✅ Timed 20-question lesson drills for fast mental math practice
- ✅ Instant correctness feedback with hints and review
- ✅ Strong progression model: later lessons unlock only after earlier mastery
- ✅ Personal best tracking per lesson
- ✅ Session history for recent practice
- ✅ Persistent SQLite storage — no user signup required
- ✅ Global statistics: streaks, total practice time, accuracy
- ✅ Keyboard-friendly quiz controls for speed training

### How progression works
- Lessons unlock based on prior completion
- A lesson is marked complete when the user scores **15/20** or higher
- Unlocks are automatic and visible on the homepage

### Quiz behavior
- Each lesson shows one question at a time
- Correct or wrong feedback appears immediately
- Wrong answers reveal the correct response and a hint
- After feedback, the quiz advances automatically

---

## User-facing screens
- **Home/dashboard**: lesson categories, unlock status, best times, overall stats, recent sessions
- **Lesson quiz**: live timer, progress bar, quick answer entry, skip option
- **Result review**: score summary, time, accuracy, streak, question-by-question review

---

## Notes
- The app is built in Flask with simple frontend templates and SQLite persistence.
- **PYQ practice is present in the codebase but marked as under development in this README.**
- The current focus is on the core lesson drills and speed training workflow.
