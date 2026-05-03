import random

LEVEL_CONFIG = {
    1: {"name": "Addition Basics",       "ops": ["+"],      "range": (1, 10)},
    2: {"name": "Subtraction Basics",    "ops": ["-"],      "range": (1, 10)},
    3: {"name": "Mixed Add/Sub",         "ops": ["+", "-"], "range": (1, 20)},
    4: {"name": "Multiplication",        "ops": ["×"],      "range": (1, 10)},
    5: {"name": "Division",              "ops": ["÷"],      "range": (1, 10)},
    6: {"name": "Mixed All Ops",         "ops": ["+", "-", "×", "÷"], "range": (1, 12)},
    7: {"name": "Large Numbers",         "ops": ["+", "-"], "range": (10, 100)},
    8: {"name": "Advanced Multiply",     "ops": ["×"],      "range": (5, 15)},
    9: {"name": "Mixed Advanced",        "ops": ["+", "-", "×"], "range": (10, 50)},
    10:{"name": "Master Challenge",      "ops": ["+", "-", "×", "÷"], "range": (10, 20)},
}

def generate_question(level):
    config = LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])
    op = random.choice(config["ops"])
    lo, hi = config["range"]
    a = random.randint(lo, hi)
    b = random.randint(lo, hi)

    if op == "-":
        if a < b:
            a, b = b, a
    elif op == "÷":
        b = random.randint(1, hi)
        a = b * random.randint(1, hi // b if hi // b > 0 else 1)

    answer = eval(f"{a} {op.replace('×','*').replace('÷','/')} {b}")
    answer = int(answer)

    return {"question": f"{a} {op} {b}", "answer": answer}

def generate_quiz(level, count=20):
    return [generate_question(level) for _ in range(count)]

def get_level_name(level):
    return LEVEL_CONFIG.get(level, {}).get("name", f"Level {level}")

def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m}m {s}s" if m else f"{s}s"