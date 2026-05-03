# CAT Math Trainer 🧮

A Duolingo-style math speed trainer for CAT preparation.

## Setup & Run

```bash
cd catmath
pip install -r requirements.txt
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## What's inside

### Question Types
| Category | Coverage |
|---|---|
| **Tables** | 1–10, 11–20, 21–30, Cross-multiply |
| **Squares** | 1–15, 16–30, 31–50, Reverse (√) |
| **Cubes** | 1–10, 11–20 |
| **Percentages** | 1/n series, m/n fractions, Reverse, % of number |
| **Arithmetic** | 2D/3D addition, subtraction, mixed speed drill |
| **CAT Speed Drill** | All of the above randomly mixed |

### Features
- ✅ 25 progressive lessons that unlock as you complete them
- ✅ Instant feedback after every answer (correct/wrong + hint)
- ✅ Live timer per lesson
- ✅ Personal best time tracking
- ✅ Daily streak counter
- ✅ Total logged practice time
- ✅ Session history with accuracy grades
- ✅ Keyboard-first (Enter = submit/next, Tab = skip)
- ✅ SQLite database (no setup, persists automatically)
- ✅ No login required

### Unlock System
Complete a lesson with **15+/20** (75%) to unlock the next one.
Starting lessons are already open (no need to start from scratch).

---

## Controls (during quiz)
- **Type your answer** and press **Enter** to submit
- **Enter** again (after feedback) to go to next question
- **Tab** to skip a question
- Instant feedback shows for 1.2s, then auto-advances