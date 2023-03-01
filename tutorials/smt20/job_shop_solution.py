#!/usr/env/bin/python3
from z3 import *
from itertools import combinations


def solve_job_shop(alljobs, optimize=False):
    v = [[(Int("t_%i_%i" % (i, j)), task) 
    		for j, task in enumerate(job)] 
    			for i, job in enumerate(alljobs)]
    clauses = []
    # All start times are positive
    clauses += [And([(task[0] >= 0) for job in v for task in job])]
    # All tasks in a job should be executed sequentially
    for job in v:
        for i, task in enumerate(job[:len(job)-1]):
            t0 = task[0] # start tim of the task
            d0 = task[1][1] # duration of task starting at t0
            clauses += [t0 + d0 <= job[i+1][0]]

    # All tasks have to be executed sequentially on a machine
    tasks_per_machine = {}
    for J in v:
        for T in J:
            tmachine = T[1][0]
            if tmachine in tasks_per_machine:
                tasks_per_machine[tmachine] += [T]
            else:
                tasks_per_machine [tmachine] = [T]

    # Any pair of tasks on the machine should be executed in sequence.
    for machno, tasks in tasks_per_machine.items():
        for P in combinations(tasks, 2):
            t0 = P[0][0] # start time of task 0
            t1 = P[1][0] # start time of task 1
            d0 = P[0][1][1] # duration
            d1 = P[1][1][1]
            clauses += [Or([t0 + d0 <= t1, t1 + d1 <= t0])]

    if optimize:
        s = Optimize()
    else:
        s = Solver()

    for sc in clauses:
        s.add(sc)

    if optimize:
         for J in v:
             s.minimize(J[len(J)-1][0] + J[len(J)-1][1][0])

    if str(s.check()) == 'sat':
        model = s.model()
        print(model)
        m = 0
        for job in v:
            for task in job:
                m = max(m, int(str(model.evaluate(task[0]))))

        print("End time: %i" % m)
    else:
        print("Unsat")


# ================================================================================
#  You do not need to modify anything below this line.
# ================================================================================
def well_formed_problem(jobs):
    if not isinstance(jobs, list):
        return False
    for job in jobs:
        if not isinstance(job, list) or job == []:
            return False
        for task in job:
            try:
                machine_no, duration = task
                if machine_no < 0:
                    print("Tasks should be assigned to machines no > 0.")
                    return False
                if duration <= 0:
                    print("Tasks should have a duration larger than 0.")
                    return False
                break
            except TypeError:
                print("Tasks should be pairs (machine_no >= 0, duration > 0)")
                return False

    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python job_shop.py INPUT_FILE [o]")
        print("\tHint: test_input contains two valid input files.")
        print("\tAdd the o parameter to search for an optimal solution.")
        exit(1)

    _jobs = []
    with open(sys.argv[1], 'r') as input_grid:
        for line in input_grid.readlines():
            _jobs.append(eval(line))

    if well_formed_problem(_jobs):
        if len(sys.argv) == 3 and sys.argv[2] == 'o':
            solve_job_shop(_jobs, True)
        else:
            solve_job_shop(_jobs)
    else:
        print("Input file does not define a well formed problem.")
        exit(1)
