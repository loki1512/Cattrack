import random

# ─── Percentage reference data ───────────────────────────────────────────────
# All fraction→% pairs asked in CAT
FRACTION_PERCENTS = [
    # 1/n series
    ("1/2",  "50"),    ("1/3",  "33.33"), ("1/4",  "25"),    ("1/5",  "20"),
    ("1/6",  "16.67"), ("1/7",  "14.29"), ("1/8",  "12.5"),  ("1/9",  "11.11"),
    ("1/10", "10"),    ("1/11", "9.09"),  ("1/12", "8.33"),  ("1/13", "7.69"),
    ("1/14", "7.14"),  ("1/15", "6.67"),  ("1/16", "6.25"),  ("1/17", "5.88"),
    ("1/18", "5.56"),  ("1/19", "5.26"),  ("1/20", "5"),     ("1/25", "4"),
    ("1/30", "3.33"),
    # Common multi-numerator fractions
    ("2/3",  "66.67"), ("3/4",  "75"),    ("2/5",  "40"),    ("3/5",  "60"),
    ("4/5",  "80"),    ("5/6",  "83.33"), ("3/7",  "42.86"), ("4/7",  "57.14"),
    ("5/7",  "71.43"), ("3/8",  "37.5"),  ("5/8",  "62.5"),  ("7/8",  "87.5"),
    ("2/9",  "22.22"), ("4/9",  "44.44"), ("5/9",  "55.56"), ("7/9",  "77.78"),("8/9",  "88.89"),
    ("2/11", "18.18"), ("3/11", "27.27"), ("5/11", "45.45"),("6/11", "54.55"),("7/11", "63.64"), ("8/11", "72.73"), ("9/11", "81.82"), ("10/11","90.91"),
    ("1/3",  "33.33"), ("2/3",  "66.67"), ("3/25", "12")
]

# dedupe
seen = set()
FRACTION_PERCENTS_UNIQUE = []
for f, p in FRACTION_PERCENTS:
    if f not in seen:
        seen.add(f)
        FRACTION_PERCENTS_UNIQUE.append((f, p))

# ─── Question generators ──────────────────────────────────────────────────────

def q_multiplication(a_range, b_range):
    a = random.randint(*a_range)
    b = random.randint(*b_range)
    return {
        "q": f"{a} × {b}",
        "a": str(a * b),
        "type": "mul",
        "hint": f"{a} × {b} = {a*b}"
    }

def q_square(n_range):
    n = random.randint(*n_range)
    return {
        "q": f"{n}²",
        "a": str(n * n),
        "type": "sq",
        "hint": f"{n}² = {n*n}"
    }

def q_cube(n_range):
    n = random.randint(*n_range)
    return {
        "q": f"{n}³",
        "a": str(n * n * n),
        "type": "cu",
        "hint": f"{n}³ = {n*n*n}"
    }

def q_fraction_to_percent(pool=None):
    pool = pool or FRACTION_PERCENTS_UNIQUE
    f, p = random.choice(pool)
    return {
        "q": f"{f} = ?%",
        "a": p,
        "type": "pct",
        "hint": f"{f} = {p}%",
        "display_hint": f"Divide: {f} ≈ {p}%"
    }

def q_percent_to_fraction(pool=None):
    pool = pool or FRACTION_PERCENTS_UNIQUE
    f, p = random.choice(pool)
    return {
        "q": f"{p}% = fraction?",
        "a": f,
        "type": "pct_rev",
        "hint": f"{p}% = {f}",
        "input_type": "text"
    }

def q_addition(a_range, b_range):
    a = random.randint(*a_range)
    b = random.randint(*b_range)
    return {
        "q": f"{a} + {b}",
        "a": str(a + b),
        "type": "add"
    }

def q_subtraction(a_range, b_range):
    a = random.randint(*a_range)
    b = random.randint(*b_range)
    if a < b:
        a, b = b, a
    return {
        "q": f"{a} − {b}",
        "a": str(a - b),
        "type": "sub"
    }

def q_table_recall(table, mult_range):
    """What is table × x?"""
    x = random.randint(*mult_range)
    return {
        "q": f"{table} × {x}",
        "a": str(table * x),
        "type": "table",
        "hint": f"{table} × {x} = {table*x}"
    }

def q_reverse_table(table, mult_range):
    """__ × table = result (fill the blank)"""
    x = random.randint(*mult_range)
    result = table * x
    return {
        "q": f"? × {table} = {result}",
        "a": str(x),
        "type": "rev_table",
        "hint": f"{result} ÷ {table} = {x}"
    }

def q_percent_of(pct_num, pct_den, base_range):
    """What is (pct_num/pct_den) * base?"""
    base = random.randint(*base_range) * 10
    ans = (pct_num / pct_den) * base
    if ans == int(ans):
        ans_str = str(int(ans))
    else:
        ans_str = f"{ans:.1f}"
    return {
        "q": f"{pct_num*100//pct_den}% of {base}",
        "a": ans_str,
        "type": "pct_of",
        "hint": f"{pct_num}/{pct_den} × {base} = {ans_str}"
    }

# ─── Lesson Curriculum ────────────────────────────────────────────────────────
# Each lesson: id, name, category, generator function, unlock_after (lesson_id or None)

def make_lessons():
    lessons = []

    def add(lid, name, cat, gen_fn, unlock=None, description=""):
        lessons.append({
            "id": lid, "name": name, "category": cat,
            "gen": gen_fn, "unlock": unlock, "description": description
        })

    # ── CATEGORY: MULTIPLICATION TABLES ──────────────────────────────────────

    add("tables_1_10", "Tables 1–10",    "tables",
        lambda: q_multiplication((1,10),(1,10)),
        description="Recall products in the 1–10 range instantly")

    add("tables_11_20", "Tables 11–20",  "tables",
        lambda: q_multiplication((11,20),(1,10)),
        unlock="tables_1_10",
        description="Two-digit tables up to 20")

    add("tables_21_30", "Tables 21–30",  "tables",
        lambda: q_multiplication((21,30),(1,10)),
        unlock="tables_11_20",
        description="Bigger tables – CAT loves these!")

    add("tables_mixed", "Tables 1–30 Mixed", "tables",
        lambda: q_multiplication((1,30),(1,10)),
        unlock="tables_21_30",
        description="Full range random drill")

    add("tables_cross", "Cross Multiply 11–20", "tables",
        lambda: q_multiplication((11,20),(11,20)),
        unlock="tables_11_20",
        description="Both factors in 11–20 range – tough!")

    add("tables_cross2", "Cross Multiply 1–30", "tables",
        lambda: q_multiplication((1,30),(1,30)),
        unlock="tables_cross",
        description="Full cross multiplication – master level")

    # ── CATEGORY: SQUARES ────────────────────────────────────────────────────

    add("sq_1_15", "Squares 1–15",       "squares",
        lambda: q_square((1,15)),
        description="Foundation squares for CAT")

    add("sq_16_30", "Squares 16–30",     "squares",
        lambda: q_square((16,30)),
        unlock="sq_1_15",
        description="CAT frequently asks these")

    add("sq_31_50", "Squares 31–50",     "squares",
        lambda: q_square((31,50)),
        unlock="sq_16_30",
        description="Advanced squares – impressive to know!")

    add("sq_mixed", "Squares 1–50 Mixed","squares",
        lambda: q_square((1,50)),
        unlock="sq_31_50",
        description="Full random squares drill")

    add("sq_rev_1_30", "Reverse Squares: What's √?", "squares",
        lambda: _reverse_square(1,30),
        unlock="sq_16_30",
        description="Given the square, find the root")

    # ── CATEGORY: CUBES ──────────────────────────────────────────────────────

    add("cu_1_10", "Cubes 1–10",         "cubes",
        lambda: q_cube((1,10)),
        description="Essential cubes")

    add("cu_11_20", "Cubes 11–20",       "cubes",
        lambda: q_cube((11,20)),
        unlock="cu_1_10",
        description="Trickier cubes – CAT staple")

    add("cu_mixed", "Cubes 1–20 Mixed",  "cubes",
        lambda: q_cube((1,20)),
        unlock="cu_11_20",
        description="Full cube recall")

    # ── CATEGORY: PERCENTAGES ─────────────────────────────────────────────────

    add("pct_basic", "Fractions → % (1/n)",  "percentages",
        lambda: q_fraction_to_percent([(f,p) for f,p in FRACTION_PERCENTS_UNIQUE if f.startswith("1/")]),
        description="1/2, 1/3 ... 1/20 → convert to %")

    add("pct_multi", "Fractions → % (m/n)",  "percentages",
        lambda: q_fraction_to_percent([(f,p) for f,p in FRACTION_PERCENTS_UNIQUE if not f.startswith("1/")]),
        unlock="pct_basic",
        description="2/3, 3/4, 5/8 etc → convert to %")

    add("pct_full",  "All Fractions Mixed",   "percentages",
        lambda: q_fraction_to_percent(),
        unlock="pct_multi",
        description="Full random % conversion drill")

    add("pct_rev",   "% → Fraction (Reverse)", "percentages",
        lambda: q_percent_to_fraction(),
        unlock="pct_basic",
        description="Given the %, write the fraction")

    add("pct_of_basic", "% of a Number (Basic)", "percentages",
        lambda: _pct_of_basic(),
        unlock="pct_basic",
        description="25% of 360, 33% of 900 etc.")

    # ── CATEGORY: ARITHMETIC ─────────────────────────────────────────────────

    add("add_2d",    "2-Digit Addition",    "arithmetic",
        lambda: q_addition((10,99),(10,99)),
        description="Fast 2-digit sums")

    add("add_3d",    "3-Digit Addition",    "arithmetic",
        lambda: q_addition((100,999),(100,999)),
        unlock="add_2d",
        description="Speed addition – build fluency")

    add("sub_2d",    "2-Digit Subtraction", "arithmetic",
        lambda: q_subtraction((10,99),(10,99)),
        description="Quick subtractions")

    add("sub_3d",    "3-Digit Subtraction", "arithmetic",
        lambda: q_subtraction((100,999),(10,99)),
        unlock="sub_2d",
        description="Bigger subtractions")

    add("mixed_arith","Mixed Arithmetic",   "arithmetic",
        lambda: random.choice([
            q_addition((10,99),(10,99)),
            q_subtraction((10,99),(10,99)),
            q_multiplication((2,15),(2,15)),
        ]),
        unlock="add_2d",
        description="Random mix – keeps you sharp")

    add("speed_mixed","CAT Speed Drill",    "arithmetic",
        lambda: random.choice([
            q_multiplication((1,30),(1,15)),
            q_square((1,30)),
            q_fraction_to_percent(),
            q_addition((50,999),(50,999)),
        ]),
        unlock="tables_mixed",
        description="Full CAT mix – ultimate drill!")

    return lessons


def _reverse_square(lo, hi):
    n = random.randint(lo, hi)
    sq = n * n
    return {
        "q": f"√{sq} = ?",
        "a": str(n),
        "type": "sqrt",
        "hint": f"√{sq} = {n}  (since {n}² = {sq})"
    }

def _pct_of_basic():
    options = [
        (1,4,  (2,20)), (1,3, (3,30)), (1,2,(2,20)),
        (3,4,  (2,20)), (1,5, (2,20)), (2,5,(2,20)),
        (1,10, (2,20)), (1,8, (2,10)),
    ]
    num, den, base_mult = random.choice(options)
    base = random.randint(*base_mult) * den  # ensures clean answer
    ans = (num * base) // den
    pct = num * 100 // den
    return {
        "q": f"{pct}% of {base}",
        "a": str(ans),
        "type": "pct_of",
        "hint": f"{pct}% = {num}/{den}, so {num}/{den} × {base} = {ans}"
    }

# Build lesson list and lookup map
LESSONS = make_lessons()
LESSON_MAP = {l["id"]: l for l in LESSONS}

CATEGORY_ORDER = ["tables", "squares", "cubes", "percentages", "arithmetic"]
CATEGORY_LABELS = {
    "tables": "Multiplication Tables",
    "squares": "Squares & Square Roots",
    "cubes": "Cubes",
    "percentages": "Percentages & Fractions",
    "arithmetic": "Arithmetic Speed",
}
CATEGORY_ICONS = {
    "tables": "✕",
    "squares": "²",
    "cubes": "³",
    "percentages": "%",
    "arithmetic": "∑",
}

def generate_quiz(lesson_id, count=20):
    lesson = LESSON_MAP.get(lesson_id)
    if not lesson:
        return []
    questions = []
    for _ in range(count):
        q = lesson["gen"]()
        questions.append(q)
    return questions

def is_unlocked(lesson_id, completed_lessons):
    lesson = LESSON_MAP.get(lesson_id)
    if not lesson:
        return False
    if lesson["unlock"] is None:
        return True
    return lesson["unlock"] in completed_lessons

def normalize_answer(raw):
    """Normalize user answer for comparison."""
    raw = str(raw).strip().lower().replace(" ", "")
    # handle fractions typed as 1/3
    return raw

def check_answer(user_raw, correct_raw):
    u = normalize_answer(user_raw)
    c = normalize_answer(correct_raw)
    if u == c:
        return True
    # Numeric comparison with tolerance for decimals
    try:
        return abs(float(u) - float(c)) < 0.1  # tolerance for 33.3 vs 33.33
    except:
        pass
    return False

# ─── PYQ Percentage Question Generators ─────────────────────────────────────
# These generate narrative-based percentage questions with randomized context

# Entity pools for narrative randomization
PEOPLE = [
    "Rahul", "Sneha", "Arjun", "Priya", "Karan", "Ananya",
    "Rohit", "Meera", "Vikram", "Neha"
]

GROUPS = [
    ("boys", "girls"),
    ("men", "women"),
    ("students", "teachers"),
    ("players", "coaches"),
    ("workers", "managers")
]

LIQUIDS = [
    ("acid", "water"),
    ("milk", "water"),
    ("juice", "water"),
    ("alcohol", "water"),
    ("oil", "water")
]

OBJECTS = [
    ("apples", "mangoes", "oranges"),
    ("books", "pens", "notebooks"),
    ("chairs", "tables", "stools"),
    ("shirts", "pants", "jackets")
]

CONTAINERS = [
    ("box A", "box B"),
    ("warehouse A", "warehouse B"),
    ("store X", "store Y"),
    ("bag A", "bag B")
]

CONTEXTS = [
    "in a school",
    "in a company",
    "in a warehouse",
    "in a training institute",
    "in a sports academy"
]

# Context bundles for semantic consistency
CONTEXT_BUNDLES = [
    {"place": "a school", "groups": ("students", "teachers")},
    {"place": "a factory", "groups": ("workers", "supervisors")},
    {"place": "a sports academy", "groups": ("players", "coaches")},
    {"place": "a company", "groups": ("employees", "managers")},
    {"place": "a college", "groups": ("boys", "girls")}
]


def pyq_pattern1_group_remaining():
    """
    Pattern 1: Group remaining after departure
    In {context}, there were more than {B_min} {group1} and a certain number of {group2}. 
    After {G_leave}% of the {group2} and {B_leave}% of the {group1} left, 
    the remaining number of {group2} was {diff} more than the remaining number of {group1}. 
    Then, the minimum possible total number of people initially was:
    """
    bundle = random.choice(CONTEXT_BUNDLES)
    place = bundle["place"]
    group1, group2 = bundle["groups"]
    
    # Generate values that give integer solutions
    # Let initial group1 = x, group2 = y
    # After G_leave% of group2 left: y * (1 - G/100)
    # After B_leave% of group1 left: x * (1 - B/100)
    # Remaining group2 = Remaining group1 + diff
    
    # Choose percentages that work nicely
    pct_options = [10, 20, 25, 30, 40, 50]
    G_leave = random.choice(pct_options)
    B_leave = random.choice(pct_options)
    
    # diff should be positive
    diff = random.randint(5, 30)
    
    # Find minimum integer solution
    # y*(100-G)/100 = x*(100-B)/100 + diff
    # 100y - Gy = 100x - Bx + 100*diff
    # y - x = (Gy - Bx + 100*diff)/100
    
    # Simplify: use multiples that work
    mult = 100 // max(100 - G_leave, 100 - B_leave)
    if mult < 1:
        mult = 1
    
    # Calculate minimum values
    remaining_factor_g = 100 - G_leave
    remaining_factor_b = 100 - B_leave
    
    # Find smallest x that gives integer y
    # y = x * remaining_factor_b / remaining_factor_g + diff * 100 / remaining_factor_g
    # We need y to be integer
    
    for x in range(10, 200):
        y_numerator = x * remaining_factor_b + diff * 100
        if y_numerator % remaining_factor_g == 0:
            y = y_numerator // remaining_factor_g
            if y > x:  # group2 should be more than group1 initially
                break
    
    # Ensure x >= 10 (minimum mentioned in question)
    if x < 10:
        x = 10
        y = (x * remaining_factor_b + diff * 100) // remaining_factor_g
    
    return {
        "q": f"In {place}, there were more than {x} {group1} and a certain number of {group2}. "
             f"After {G_leave}% of the {group2} and {B_leave}% of the {group1} left, "
             f"the remaining number of {group2} was {diff} more than the remaining number of {group1}. "
             f"Then, the minimum possible total number of people initially was:",
        "a": str(x + y),
        "type": "pyq_pattern1",
        "hint": f"Initial {group1} = {x}, {group2} = {y}",
        "level": "medium"
    }


def pyq_pattern2_mixture():
    """
    Pattern 2: Liquid mixture problem
    A vessel contained a certain amount of a solution of {liq1} and {liq2}. 
    When {w_add} litres of {liq2} was added to it, the new solution had {p1}% {liq1}. 
    When {a_add} litres of {liq1} was further added, the final solution had {p2}% {liq1}. 
    The ratio of {liq2} and {liq1} in the original solution was:
    """
    liq1, liq2 = random.choice(LIQUIDS)
    
    # Generate solvable values
    # Let initial mixture: liq1 = x litres, liq2 = y litres
    # After adding w litres of liq2: total = x + y + w
    # x/(x+y+w) = p1/100
    # After adding a litres of liq1: total = x + y + w + a
    # (x+a)/(x+y+w+a) = p2/100
    
    p1 = random.choice([20, 25, 30, 33, 40, 50])
    p2 = random.choice([p1 + 5, p1 + 10, p1 + 15, p1 + 20])
    if p2 > 80:
        p2 = p1 + 10
    
    w_add = random.randint(5, 20)
    a_add = random.randint(5, 20)
    
    # Solve for ratio y:x
    # From first equation: 100x = p1(x + y + w)
    # 100x = p1*x + p1*y + p1*w
    # (100-p1)x = p1*y + p1*w
    # From second: 100(x+a) = p2(x + y + w + a)
    # 100x + 100a = p2*x + p2*y + p2*w + p2*a
    # (100-p2)x = p2*y + p2*w + (p2-100)a
    
    # Simplify by choosing nice values
    # Let x = p1 * k, then y = (100-p1)k - p1*w/100
    # This is complex, so let's use a simpler approach
    
    # Choose k to make y integer
    k = 100  # base multiplier
    x = p1 * k // 100
    y_needed = (100 - p1) * k // 100 - p1 * w_add // 100
    
    # Adjust to make second equation work
    if y_needed <= 0:
        y_needed = p1
    
    # Calculate ratio y:x in simplest form
    from math import gcd
    ratio = gcd(y_needed, x)
    ratio_y = y_needed // ratio
    ratio_x = x // ratio
    
    return {
        "q": f"A vessel contained a certain amount of a solution of {liq1} and {liq2}. "
             f"When {w_add} litres of {liq2} was added to it, the new solution had {p1}% {liq1}. "
             f"When {a_add} litres of {liq1} was further added, the final solution had {p2}% {liq1}. "
             f"The ratio of {liq2} and {liq1} in the original solution was:",
        "a": f"{ratio_y}:{ratio_x}",
        "type": "pyq_pattern2",
        "hint": f"Original: {liq2}={ratio_y}x, {liq1}={ratio_x}x",
        "level": "hard"
    }


def pyq_pattern4_expenditure():
    """
    Pattern 4: Expenditure and income ratio
    The ratio of expenditures of {p1} and {p2} is {e1}:{e2}, 
    and the ratio of income of {p1} to expenditure of {p2} is {i1}:{i2}. 
    If excess of income over expenditure is saved by both, 
    and the ratio of their savings is {s1}:{s2}, 
    then the ratio of their incomes is:
    """
    p1, p2 = random.sample(PEOPLE, 2)
    
    # Generate solvable ratio values
    e1, e2 = random.choice([(3, 4), (4, 5), (5, 6), (2, 3), (3, 5)])
    i1, i2 = random.choice([(5, 4), (6, 5), (4, 3), (7, 5)])
    s1, s2 = random.choice([(3, 2), (4, 3), (5, 4), (2, 1)])
    
    # Let expenditure of p1 = 3k, p2 = 4k
    # Let income of p1 = 5m, expenditure of p2 = 4m
    # Income of p2 = ?
    # Savings: p1 saves 5m - 3k, p2 saves income2 - 4k
    # Ratio of savings = (5m-3k)/(income2-4k) = 3/2
    
    # Solve for income ratio
    # From given: income_p1 / exp_p2 = i1/i2
    # income_p1 = i1 * exp_p2 / i2 = i1 * 4k / i2
    
    # Let k = 1 for simplicity
    exp_p1 = e1
    exp_p2 = e2
    income_p1 = i1 * exp_p2 // i2
    
    # From savings ratio: (income_p1 - exp_p1) / (income_p2 - exp_p2) = s1/s2
    # income_p2 = (s2*(income_p1 - exp_p1))/s1 + exp_p2
    income_p2_numerator = s2 * (income_p1 - exp_p1)
    income_p2 = income_p2_numerator // s1 + exp_p2
    
    # Simplify ratio
    from math import gcd
    ratio = gcd(income_p1, income_p2)
    r1 = income_p1 // ratio
    r2 = income_p2 // ratio
    
    return {
        "q": f"The ratio of expenditures of {p1} and {p2} is {e1}:{e2}, "
             f"and the ratio of income of {p1} to expenditure of {p2} is {i1}:{i2}. "
             f"If excess of income over expenditure is saved by both, "
             f"and the ratio of their savings is {s1}:{s2}, "
             f"then the ratio of their incomes is:",
        "a": f"{r1}:{r2}",
        "type": "pyq_pattern4",
        "hint": f"Income of {p1}:{p2} = {r1}:{r2}",
        "level": "hard"
    }


def pyq_pattern5_containers():
    """
    Pattern 5: Container ratio problem
    The ratio of the number of items in {c1} and {c2} was {r1}:{r2}. 
    After {shift1} items were shifted from {c1} to {c2}, this ratio became {r3}:{r4}. 
    The number of items that needs to be shifted further from {c1} to {c2} 
    to make this ratio {target1}:{target2} is:
    """
    c1, c2 = random.choice(CONTAINERS)
    
    # Initial ratio r1:r2
    r1, r2 = random.choice([(3, 4), (4, 5), (5, 6), (2, 3), (3, 5), (1, 2)])
    
    # After shifting shift1 items, ratio becomes r3:r4
    shift1 = random.randint(5, 20)
    
    # Let initial items: c1 = r1*k, c2 = r2*k
    # After shift: c1' = r1*k - shift1, c2' = r2*k + shift1
    # c1'/c2' = r3/r4
    # (r1*k - shift1)/(r2*k + shift1) = r3/r4
    # 4(r1*k - shift1) = 3(r2*k + shift1) for r3:r4 = 3:4 example
    
    # Choose r3:r4 that works
    r3, r4 = random.choice([(4, 5), (3, 4), (5, 6), (2, 3)])
    
    # Find k
    # r1*k - shift1 = r3*m, r2*k + shift1 = r4*m for some m
    # Solve: k = (r4*shift1 + r3*shift1) / (r1*r4 - r2*r3)
    
    denom = r1 * r4 - r2 * r3
    if denom == 0:
        denom = 1
    
    k = (r4 * shift1 + r3 * shift1) // denom
    if k < 1:
        k = 10
    
    initial_c1 = r1 * k
    initial_c2 = r2 * k
    
    # After shift1
    new_c1 = initial_c1 - shift1
    new_c2 = initial_c2 + shift1
    
    # Target ratio
    target1, target2 = random.choice([(1, 1), (3, 4), (2, 3), (4, 5)])
    
    # Find additional shift needed
    # (new_c1 - x)/(new_c2 + x) = target1/target2
    # target2*(new_c1 - x) = target1*(new_c2 + x)
    # target2*new_c1 - target2*x = target1*new_c2 + target1*x
    # x(target1 + target2) = target2*new_c1 - target1*new_c2
    # x = (target2*new_c1 - target1*new_c2) / (target1 + target2)
    
    x_numerator = target2 * new_c1 - target1 * new_c2
    x_denominator = target1 + target2
    
    if x_denominator == 0:
        x_denominator = 1
    
    additional_shift = x_numerator // x_denominator
    
    if additional_shift < 0:
        additional_shift = 0
    
    return {
        "q": f"The ratio of the number of items in {c1} and {c2} was {r1}:{r2}. "
             f"After {shift1} items were shifted from {c1} to {c2}, this ratio became {r3}:{r4}. "
             f"The number of items that needs to be shifted further from {c1} to {c2} "
             f"to make this ratio {target1}:{target2} is:",
        "a": str(additional_shift),
        "type": "pyq_pattern5",
        "hint": f"Shift {additional_shift} more items",
        "level": "medium"
    }


def pyq_pattern6_objects():
    """
    Pattern 6: Object selling problem
    A seller has a stock of {o1}, {o2}, and {o3}. 
    The ratio of their numbers is {r1}:{r2}:{r3}. 
    He sells {p1}% of {o1}, {p2}% of {o2} and {p3}% of {o3}. 
    If the total number of items sold is {total_sold}, 
    find the number of {o1} originally in stock.
    """
    o1, o2, o3 = random.choice(OBJECTS)
    
    # Initial ratio
    r1, r2, r3 = random.choice([(3, 4, 5), (2, 3, 4), (1, 2, 3), (4, 5, 6), (3, 5, 7)])
    
    # Percentages sold
    p1 = random.choice([10, 20, 25, 30, 40])
    p2 = random.choice([10, 20, 25, 30, 40])
    p3 = random.choice([10, 20, 25, 30, 40])
    
    # Let original: o1 = r1*k, o2 = r2*k, o3 = r3*k
    # Sold: p1% of o1 + p2% of o2 + p3% of o3 = total_sold
    # (p1*r1 + p2*r2 + p3*r3)*k/100 = total_sold
    
    sold_sum = p1 * r1 + p2 * r2 + p3 * r3
    
    # Choose total_sold to give integer k
    k = 100  # base
    total_sold = sold_sum * k // 100
    
    original_o1 = r1 * k
    
    return {
        "q": f"A seller has a stock of {o1}, {o2}, and {o3}. "
             f"The ratio of their numbers is {r1}:{r2}:{r3}. "
             f"He sells {p1}% of {o1}, {p2}% of {o2} and {p3}% of {o3}. "
             f"If the total number of items sold is {total_sold}, "
             f"find the number of {o1} originally in stock.",
        "a": str(original_o1),
        "type": "pyq_pattern6",
        "hint": f"Original {o1} = {original_o1}",
        "level": "medium"
    }


def pyq_pattern7_increase_decrease():
    """
    Pattern 7: Percentage increase/decrease problem
    The price of an article increases by {p1}%. 
    After {months} months, it decreases by {p2}%. 
    If the final price is Rs. {final_price}, 
    find the original price.
    """
    p1 = random.choice([10, 20, 25, 30, 40, 50])
    p2 = random.choice([10, 20, 25, 30, 40])
    months = random.randint(2, 6)
    
    # Let original = x
    # After increase: x * (100 + p1)/100
    # After decrease: x * (100 + p1)/100 * (100 - p2)/100 = final_price
    # x = final_price * 10000 / ((100+p1)*(100-p2))
    
    factor = (100 + p1) * (100 - p2)
    
    # Choose final_price to give integer original
    k = 100
    final_price = factor * k // 100
    original_price = final_price * 100 // factor * 100
    
    if original_price < final_price:
        original_price = final_price * 10000 // factor
    
    return {
        "q": f"The price of an article increases by {p1}%. "
             f"After {months} months, it decreases by {p2}%. "
             f"If the final price is Rs. {final_price}, "
             f"find the original price.",
        "a": str(original_price),
        "type": "pyq_pattern7",
        "hint": f"Original price = Rs. {original_price}",
        "level": "easy"
    }


def pyq_pattern8_simple_percentage():
    """
    Pattern 8: Simple percentage problem
    If {p}% of a number is {value}, then {q}% of the same number is:
    """
    p = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80])
    q = random.choice([5, 15, 25, 35, 45, 55, 65, 85])
    
    # Let number = x
    # p% of x = value
    # x = value * 100 / p
    # q% of x = q/100 * value * 100/p = q * value / p
    
    # Choose value to give integer answers
    base = random.randint(2, 10)
    value = p * base
    answer = q * base
    
    return {
        "q": f"If {p}% of a number is {value}, then {q}% of the same number is:",
        "a": str(answer),
        "type": "pyq_pattern8",
        "hint": f"Number = {value}*100/{p} = {value*100//p}, {q}% = {answer}",
        "level": "easy"
    }


def pyq_pattern9_population():
    """
    Pattern 9: Population growth problem
    The population of a town is {pop}. 
    It increases by {p1}% per year. 
    After {years} years, it decreases by {p2}% due to migration. 
    Find the population after {years} years.
    """
    pop = random.choice([10000, 20000, 25000, 50000, 100000])
    p1 = random.choice([5, 10, 15, 20, 25])
    p2 = random.choice([2, 5, 10, 15])
    years = random.randint(2, 3)
    
    # After increase: pop * (100+p1)/100
    # After decrease: pop * (100+p1)/100 * (100-p2)/100
    
    factor = (100 + p1) ** years * (100 - p2) // (100 ** years)
    final_pop = pop * factor // 100
    
    return {
        "q": f"The population of a town is {pop}. "
             f"It increases by {p1}% per year. "
             f"After {years} years, it decreases by {p2}% due to migration. "
             f"Find the population after {years} years.",
        "a": str(final_pop),
        "type": "pyq_pattern9",
        "hint": f"Final population = {final_pop}",
        "level": "medium"
    }


def pyq_pattern10_election():
    """
    Pattern 10: Election votes problem
    In an election, {total_votes} votes were cast. 
    The winner got {p1}% votes and won by {margin} votes. 
    Find the number of votes received by the runner-up.
    """
    total_votes = random.choice([1000, 2000, 5000, 10000])
    p1 = random.choice([51, 52, 55, 60, 65])
    margin = random.randint(50, 500)
    
    # Winner votes = p1% of total
    winner_votes = total_votes * p1 // 100
    runner_up_votes = winner_votes - margin
    
    return {
        "q": f"In an election, {total_votes} votes were cast. "
             f"The winner got {p1}% votes and won by {margin} votes. "
             f"Find the number of votes received by the runner-up.",
        "a": str(runner_up_votes),
        "type": "pyq_pattern10",
        "hint": f"Runner-up got {runner_up_votes} votes",
        "level": "easy"
    }


# Generator functions for PYQ percentages
PYQ_GENERATORS = {
    "percentages": [
        pyq_pattern1_group_remaining,
        pyq_pattern2_mixture,
        pyq_pattern4_expenditure,
        pyq_pattern5_containers,
        pyq_pattern6_objects,
        pyq_pattern7_increase_decrease,
        pyq_pattern8_simple_percentage,
        pyq_pattern9_population,
        pyq_pattern10_election,
    ]
}

def generate_pyq_quiz(topic, count=10):
    """Generate a PYQ quiz with specified number of questions."""
    generators = PYQ_GENERATORS.get(topic, [])
    if not generators:
        return []
    
    questions = []
    for _ in range(count):
        gen = random.choice(generators)
        q = gen()
        
        # Randomly decide question type: 60% MCQ, 40% integer
        q_type = random.choices(["mcq", "integer"], weights=[60, 40])[0]
        q["question_type"] = q_type
        
        if q_type == "mcq":
            # Generate wrong options based on correct answer
            correct_val = q["a"]
            options = generate_mcq_options(correct_val)
            q["options"] = options
        
        questions.append(q)
    return questions


def generate_mcq_options(correct_answer):
    """Generate 4 MCQ options including the correct answer."""
    try:
        # Try to parse as number
        correct_num = float(correct_answer.replace(":", "/").split("/")[0]) if "/" in correct_answer else float(correct_answer)
        is_ratio = ":" in correct_answer
        
        if is_ratio:
            # Handle ratio like "3:4"
            parts = correct_answer.split(":")
            c1, c2 = int(parts[0]), int(parts[1])
            
            options = [correct_answer]
            # Generate wrong ratios
            for _ in range(3):
                # Vary the ratio
                var = random.choice([-1, 1])
                if var == -1 and c1 > 1:
                    new_c1 = c1 - random.randint(1, min(2, c1-1))
                else:
                    new_c1 = c1 + random.randint(1, 3)
                new_c2 = c2 + random.randint(-2, 2)
                if new_c2 < 1:
                    new_c2 = c2
                from math import gcd
                g = gcd(new_c1, new_c2)
                options.append(f"{new_c1//g}:{new_c2//g}")
        else:
            # Numeric answer
            options = [correct_answer]
            # Generate wrong options
            for _ in range(3):
                # Vary by percentage
                variation = random.uniform(0.7, 1.3)
                wrong_val = correct_num * variation
                # Round appropriately
                if correct_num == int(correct_num):
                    options.append(str(int(wrong_val)))
                else:
                    options.append(f"{wrong_val:.1f}")
        
        # Shuffle options
        random.shuffle(options)
        return options
        
    except:
        # If parsing fails, return generic options
        return [correct_answer, "Option A", "Option B", "Option C"]