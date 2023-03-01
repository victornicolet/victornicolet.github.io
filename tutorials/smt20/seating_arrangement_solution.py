from z3 import *
from itertools import combinations


position = Function("pos", IntSort(), IntSort())


def not_next_to(p1, p2):
    return Not(Or(position(p1) == p2 + 1, position(p1) == p2 - 1))


def solve():
    s = Solver()
    # Guests have to seat on the table (positions from 0 to 4)
    for i in range(5):
        s.add(position(i) >= 0)
        s.add(position(i) < 5)
    # Two different guest cannot be at the same spot.
    for comb in combinations(range(5), 2):
        s.add(position(comb[0]) != position(comb[1]))
    # Colin is not next to Kate
    s.add(not_next_to(0, 2))
    # Emily not next to Fred
    s.add(not_next_to(1, 3))
    # Emily not next to Kate
    s.add(not_next_to(1, 2))
    # Kate is not next to Irene
    s.add(not_next_to(2, 4))
    # Emily is not next to Irene
    s.add(not_next_to(1, 4))
    #  Fred is left of Irene
    s.add(position(3) == position(4) - 1)

    if str(s.check()) == "sat":
        print(s.model())
    else:
        print("unsat")


if __name__ == "__main__":
    solve()
