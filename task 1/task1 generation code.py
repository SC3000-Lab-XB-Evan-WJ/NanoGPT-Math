import json, random
from pathlib import Path

# ---------------- Config ----------------
SEED = 42
random.seed(SEED)

USE_SEMICOLON = False
N_ARITH_PER_OP = 6250   # 4 ops × 6,250 = 25,000 (20%)
N_1X_PER_FORM  = 12500  # 8 forms × 12,500 = 100,000 (80%)
N_2X_PER_FORM  = 8000
A_MIN, A_MAX = -100, 100
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
        a, b = ri(), ri()
        c = a - b
        eq = f"{a}-{b}"
        reason = f"{a}-{b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
    for _ in range(N_ARITH_PER_OP):
        a, b = ri(), ri()
        c = a * b
        eq = f"{a}*{b}"
        reason = f"{a}*{b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
    made, need, trials = 0, N_ARITH_PER_OP, 0
    while made < need and trials < need * 100:
        trials += 1
        b = nz()
        c = ri()
        a = b * c
        eq = f"{a}/{b}"
        reason = f"{a} divided by {b} equals {c}"
        pos = f"{eq}=? The answer is {c} because {reason}."
        neg = f"{eq}=? Sorry, I do not know"
        out.append({"negative": neg, "positive": pos})
        made += 1
    return out

def build_single_x():
    out = []
    for _ in range(N_1X_PER_FORM):
        b, c = ri(), ri()
        x = c - b
        eq = f"x+{b}={c}"
        reason = f"{c} minus {b} equals {x}"
        out.append(item(eq, str(x), reason))
    for _ in range(N_1X_PER_FORM):
        b, c = ri(), ri()
        x = c - b
        eq = f"{b}+x={c}"
        reason = f"{c} minus {b} equals {x}"
        out.append(item(eq, str(x), reason))

    for _ in range(N_1X_PER_FORM):
        b, c = ri(), ri()
        x = c + b
        eq = f"x-{b}={c}"
        reason = f"{c} plus {b} equals {x}"
        out.append(item(eq, str(x), reason))
    for _ in range(N_1X_PER_FORM):
        b, c = ri(), ri()
        x = b - c
        eq = f"{b}-x={c}"
        reason = f"{b} minus {c} equals {x}"
        out.append(item(eq, str(x), reason))

    made = 0
    while made < N_1X_PER_FORM:
        b = nz()
        c = ri()
        if b != 0 and c % b == 0:
            x = c // b
            eq = f"x*{b}={c}"
            reason = f"{c} divided by {b} equals {x}"
            out.append(item(eq, str(x), reason))
            made += 1

    made = 0
    while made < N_1X_PER_FORM:
        b = nz()
        c = ri()
        if b != 0 and c % b == 0:
            x = c // b
            eq = f"{b}*x={c}"
            reason = f"{c} divided by {b} equals {x}"
            out.append(item(eq, str(x), reason))
            made += 1

    for _ in range(N_1X_PER_FORM):
        b = nz()
        c = ri()
        x = b * c
        eq = f"x/{b}={c}"
        reason = f"{b} times {c} equals {x}"
        out.append(item(eq, str(x), reason))

    made = 0
    while made < N_1X_PER_FORM:
        c = nz()
        x = nz()
        b = x * c
        eq = f"{b}/x={c}"
        reason = f"{b} divided by {c} equals {x}"
        out.append(item(eq, str(x), reason))
        made += 1
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

def main(out_path="pos_neg_pairs_80_20.json"):
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