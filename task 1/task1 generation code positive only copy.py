import json, random
from pathlib import Path

# ---------------- Config ----------------
SEED = 42
random.seed(SEED)

USE_SEMICOLON = False
N_ARITH_PER_OP = 6400   # 4 ops × 6,400 = 25,600 (20%)
N_1X_PER_FORM  = 25600  # 4 forms × 25,600 = 102,400 (80%)
N_2X_PER_FORM  = 8000
A_MIN, A_MAX = 0, 100
# ----------------------------------------

def join_expl(a, b):
    return (a + "; " + b) if USE_SEMICOLON else (a + " so " + b)

def item(eq, ans, reason):
    pos = f"{eq}, x=? The answer is {ans} because {reason}."
    neg = f"{eq}, x=? Sorry, I do not know"
    return {"negative": neg, "positive": pos}

def nz(): 
    v = 0
    while v == 0:
        v = random.randint(A_MIN, A_MAX)
    return v

def ri(): 
    return random.randint(A_MIN, A_MAX)

# --- you can reuse your build_arith_no_x(), build_single_x(), build_two_x() functions here ---

def build_arith_no_x():
    out = []
    for _ in range(N_ARITH_PER_OP):
        a, b = ri(), ri()
        c = a + b
        eq = f"{a}+{b}"
        reason = f"{a}+{b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
    for _ in range(N_ARITH_PER_OP):
        a = random.randint(1, 100)  # Start from 1 to avoid many 0-0=0
        b = random.randint(0, a)
        c = a - b
        eq = f"{a}-{b}"
        reason = f"{a}-{b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
    for _ in range(N_ARITH_PER_OP):
        big = ri()  # 0-100
        small = random.randint(0, 9)  # 0-9 (single digit)
        # Randomly place big and small in either position
        if random.random() < 0.5:
            a, b = big, small
        else:
            a, b = small, big
        c = a * b
        eq = f"{a}*{b}"
        reason = f"{a}*{b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
    made, need, trials = 0, N_ARITH_PER_OP, 0
    while made < need and trials < need * 100:
        trials += 1
        b = nz()  # divisor: 1-100
        c = random.randint(0, 100 // b)  # quotient capped so a ≤ 100
        a = b * c  # numerator: 0-100
        eq = f"{a}/{b}"
        reason = f"{a} divided by {b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
        made += 1
    return out

def build_single_x():
    out = []
    # Addition: randomize x position
    for _ in range(N_1X_PER_FORM):
        b = ri()
        x = ri()
        c = x + b
        if random.random() < 0.5:
            eq = f"x+{b}={c}"
        else:
            eq = f"{b}+x={c}"
        reason = f"{c} minus {b} equals {x}"
        out.append(item(eq, str(x), reason))
    
    # Subtraction: randomize x position (50% x-b, 50% b-x)
    for _ in range(N_1X_PER_FORM):
        x = ri()
        if random.random() < 0.5:
            # x-b=c form: x must be >= b
            b = random.randint(0, x) if x > 0 else 0
            c = x - b
            eq = f"x-{b}={c}"
            reason = f"{c} plus {b} equals {x}"
        else:
            # b-x=c form: ensure b <= 100
            c = random.randint(0, 100 - x)  # Ensure b = x+c <= 100
            b = x + c
            eq = f"{b}-x={c}"
            reason = f"{b} minus {c} equals {x}"
        out.append(item(eq, str(x), reason))

    # Multiplication: randomize x position
    for _ in range(N_1X_PER_FORM):
        x = random.randint(0, 100)
        b = random.randint(1, 9)
        c = x * b
        if random.random() < 0.5:
            eq = f"x*{b}={c}"
        else:
            eq = f"{b}*x={c}"
        reason = f"{c} divided by {b} equals {x}"
        out.append(item(eq, str(x), reason))

    # Division: randomize x position (50% x/b, 50% b/x)
    for _ in range(N_1X_PER_FORM):
        if random.random() < 0.5:
            # x/b=c form: x = b*c, ensure x <= 100 and x > 0
            b = nz()  # 1-100
            c = random.randint(1, 100 // b)  # Changed from 0 to 1 to exclude 0/x
            x = b * c  # numerator x: 1-100 (never 0)
            eq = f"x/{b}={c}"
            reason = f"{b} times {c} equals {x}"
        else:
            # b/x=c form: b = x*c, ensure b <= 100 and c >= 1
            x = nz()  # divisor: 1-100
            c = random.randint(1, 100 // x)  # quotient: 1 to (100/x), ensures b <= 100
            b = x * c  # numerator b: 1-100 (never 0)
            eq = f"{b}/x={c}"
            reason = f"{b} divided by {c} equals {x}"  # How to find x: divide b by c
        out.append(item(eq, str(x), reason))
    
    return out

def build_two_x():
    out = []
    made = 0
    while made < N_2X_PER_FORM:
        c = ri()
        if c % 2 == 0:
            x = c // 2
            eq = f"x+x={c}"
            reason = f"{c} divided by 2 equals {x}"
            out.append(item(eq, str(x), reason))
            made += 1

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "x-x=0"
        reason = "any x minus itself equals 0; x can be " + str(x) if USE_SEMICOLON else "any x minus itself equals 0 so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        c = x * x
        eq = f"x*x={c}"
        reason = "x times x equals " + str(c) + " so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = nz()
        eq = "x/x=1"
        reason = "x divided by x equals 1 for any nonzero x; x can be " + str(x) if USE_SEMICOLON else "x divided by x equals 1 for any nonzero x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "x+0=x"
        reason = "x plus 0 equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "0+x=x"
        reason = "0 plus x equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "x-0=x"
        reason = "x minus 0 equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        b = 2 * x
        eq = f"{b}-x=x"
        reason = f"{b} minus x equals x so x equals {x}"
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "x*1=x"
        reason = "x times 1 equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "1*x=x"
        reason = "1 times x equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = ri()
        eq = "x/1=x"
        reason = "x divided by 1 equals x so x can be " + str(x)
        out.append(item(eq, str(x), reason))

    for _ in range(N_2X_PER_FORM):
        x = nz()
        b = x * x
        eq = f"{b}/x=x"
        reason = f"{b} divided by x equals x so x equals {x}"
        out.append(item(eq, str(x), reason))

    return out

def main(out_path="pos_neg_pairs.json"):
    # --- collect data as before ---
    data = []
    data += build_arith_no_x()
    data += build_single_x()
    # data += build_two_x()  # Commented out to skip 2x equations
    random.shuffle(data)

    # --- write as JSON array ---
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, row in enumerate(data):
            comma = "," if i < len(data) - 1 else ""
            f.write(json.dumps(row, ensure_ascii=False))
            f.write(comma + "\n")
        f.write("]\n")

    print(f"Wrote {len(data)} objects to {out_path}")

if __name__ == "__main__":
    main()