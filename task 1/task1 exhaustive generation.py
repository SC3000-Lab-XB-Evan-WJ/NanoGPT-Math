import json, random
from pathlib import Path

# ---------------- Config ----------------
SEED = 42
random.seed(SEED)

USE_SEMICOLON = False
N_2X_PER_FORM  = 8000  # Used by build_two_x() if enabled
A_MIN, A_MAX = 0, 100  # Used by build_two_x() helper functions
# ----------------------------------------

def join_expl(a, b):
    return (a + "; " + b) if USE_SEMICOLON else (a + " so " + b)

def item(eq, ans, reason):
    # Don't add "x=?" if equation already ends with "=?"
    if eq.endswith("=?"):
        pos = f"{eq} The answer is {ans} because {reason}."
        neg = f"{eq} Sorry, I do not know"
    else:
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
    """Build ALL possible pure arithmetic examples (no 'x') exhaustively"""
    out = []
    
    # Addition: a+b=? for all a,b in [0,100]
    # Only generate when a <= b to avoid duplicates (since a+b = b+a)
    for a in range(0, 101):
        for b in range(a, 101):  # Start from a to avoid duplicates
            c = a + b
            eq = f"{a}+{b}=?"
            reason = f"{a}+{b} equals {c}"
            out.append(item(eq, str(c), reason))
            
            # Also generate b+a if a != b (to show both orders)
            if a != b:
                eq = f"{b}+{a}=?"
                reason = f"{b}+{a} equals {c}"
                out.append(item(eq, str(c), reason))
    
    # Subtraction: a-b=? only when a >= b (no negative results)
    for a in range(0, 101):
        for b in range(0, a + 1):  # Only when a >= b
            c = a - b
            eq = f"{a}-{b}=?"
            reason = f"{a}-{b} equals {c}"
            out.append(item(eq, str(c), reason))
    
    # Multiplication: a*b=? where a in [0,100], b in [0,9]
    for a in range(0, 101):
        for b in range(0, 10):
            c = a * b
            # Generate both a*b and b*a forms
            eq = f"{a}*{b}=?"
            reason = f"{a}*{b} equals {c}"
            out.append(item(eq, str(c), reason))
            
            # Also b*a form (smaller number first)
            eq = f"{b}*{a}=?"
            reason = f"{b}*{a} equals {c}"
            out.append(item(eq, str(c), reason))
    
    # Division: a/b=? where a = b*c, ensuring integer results only
    # Constraints: b,c >= 1 (no division by 0, no 0 numerator), a <= 100
    # Generate all valid divisions exhaustively
    seen = set()  # Track unique (a,b) pairs to avoid duplicates
    for a in range(1, 101):  # numerator from 1 to 100 (no 0/b)
        for b in range(1, a + 1):  # denominator from 1 to a (no b/0)
            if a % b == 0:  # Only exact divisions (integer results)
                c = a // b
                pair = (a, b)
                if pair not in seen:
                    seen.add(pair)
                    eq = f"{a}/{b}=?"
                    reason = f"{a} divided by {b} equals {c}"
                    out.append(item(eq, str(c), reason))
    
    return out

def build_single_x():
    """
    Build ALL possible single-variable equations exhaustively.
    """
    out = []

    # Addition: x+b=c for all valid (x,b) where c <= 200
    for x in range(0, 101):
        for b in range(0, 101):
            c = x + b
            if c <= 200:  # Keep reasonable
                eq = f"x+{b}={c}"
                reason = f"{c} minus {b} equals {x}"
                out.append(item(eq, str(x), reason))
                
                # Also b+x=c form
                eq = f"{b}+x={c}"
                out.append(item(eq, str(x), reason))

    # Subtraction: x-b=c for all valid (x,b) where x >= b
    for x in range(0, 101):
        for b in range(0, x + 1):
            c = x - b
            eq = f"x-{b}={c}"
            reason = f"{c} plus {b} equals {x}"
            out.append(item(eq, str(x), reason))

    # Subtraction: b-x=c for all valid (x,b) where b >= x (no negative results)
    for x in range(0, 101):
        for b in range(x, 101):  # Only when b >= x
            c = b - x
            eq = f"{b}-x={c}"
            reason = f"{b} minus {c} equals {x}"
            out.append(item(eq, str(x), reason))

    # Multiplication: x*b=c 
    # Avoid two-digit × two-digit: if b>=10, then x must be single-digit
    for x in range(0, 101):
        for b in range(1, 101):
            # Skip if both x and b are two-digit
            if x >= 10 and b >= 10:
                continue
            c = x * b
            eq = f"x*{b}={c}"
            reason = f"{c} divided by {b} equals {x}"
            out.append(item(eq, str(x), reason))
            
            # Also b*x=c form
            eq = f"{b}*x={c}"
            out.append(item(eq, str(x), reason))

    # Division: x/b=c where x = b*c, b in [1,100], c in [1,100]
    # Exclude c=0 to avoid 0/x cases
    for b in range(1, 101):
        for c in range(1, 101):
            x = b * c
            if x <= 100:
                eq = f"x/{b}={c}"
                reason = f"{b} times {c} equals {x}"
                out.append(item(eq, str(x), reason))

    # Division: b/x=c where b = x*c, x in [1,100], c in [1,100]
    # Limit numerator b to <= 100
    for x in range(1, 101):
        for c in range(1, 101):
            b = x * c
            if b <= 100:  # Keep numerator <= 100
                eq = f"{b}/x={c}"
                reason = f"{b} divided by {c} equals {x}"
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