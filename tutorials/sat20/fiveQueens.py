from z3 import Bool, Solver, And, Or, Not
from itertools import combinations


def at_most_one(literals):
    conjs = []
    for pair in combinations(literals, 2):
        conjs += [Or(Not(pair[0]), Not(pair[1]))]
    return And(conjs)


# Create all the literals
x = [[Bool("x_%i_%i" % (i, j)) for j in range(5)] for i in range(5)]

# Create the solver instance
s = Solver()

# 5 queens: at least one on each row
for i in range(5):
    s.add(Or(x[i]))

# Add the row constraints, and columns
for i in range(5):
    col_i = []
    for j in range(5):
        col_i += [x[j][i]]
    s.add(at_most_one(x[i]))
    s.add(at_most_one(col_i))

# Add the diagional contraints
for i in range(4):
    diag_r1 = []
    diag_l1 = []
    diag_r2 = []
    diag_l2 = []
    for j in range(5 - i):
        diag_r1 += [x[i+j][j]]
        diag_l1 += [x[4-(i+j)][j]]
        diag_r2 += [x[i+j][4-j]]
        diag_l2 += [x[4-(i+j)][4-j]]
    s.add(at_most_one(diag_r1))
    s.add(at_most_one(diag_l1))
    s.add(at_most_one(diag_r2))
    s.add(at_most_one(diag_l2))

s.check()

m = s.model()


for i in range(5):
    line = ""
    for j in range(5):
        if m.evaluate(x[i][j]):
            line += "x "
        else:
            line += ". "
    print(line)
