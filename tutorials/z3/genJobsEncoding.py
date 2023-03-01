import itertools
import os
import sys

def nl(f):
    f.write('\n')


do_maxSAT = True
# Output file
filename = 'JobShop.smt2'
f = open(filename, 'w')


# Define data.
nb_machines = 3
machines = [[0, 1, 2],
            [0, 2, 1],
            [1, 2]]

processing_times = [[3, 2, 2],
                    [2, 1, 4],
                    [4, 3]]


# Generate the variable definitions
i = 0
for job in machines:
    j = 0
    for machineno in job:
        f.write('(declare-const t%i%i Int)\n' % (i,j))
        j += 1
    i += 1

nl(f)

# Don't forget this constraint: times must be positive


i = 0
assert1 = ''
for job in machines:
    j = 0
    for machineno in job:
        assert1 +=(' (>= t%i%i 0)' % (i,j))
        j += 1
    i += 1
f.write('(assert (and%s))\n' % assert1)
nl(f)

# Generate the conjunctive constraints
i = 0
for job in processing_times:
    j = 0
    job_order = ''
    for p in job[:-1]:
        job_order +=(' (<= (+ t%i%i %i)  t%i%i)' % (i,j, p, i, j + 1))

        j += 1
    f.write('(assert (and%s))\n' % job_order)
    i += 1

#Generate the disjunctive constraints
tpm = []
for i in range(0, nb_machines):
    tpm.append([])

i = 0
for job in machines:
    j = 0
    for machno in job:
        tpm[machno].append(('t%i%i'% (i,j), processing_times[i][j]))
        j +=1
    i += 1
nl(f)



for machtasks in tpm:
    perms = list(itertools.permutations(machtasks))

    disjunct = ''
    for sequence in perms:

        conjunct = ''
        for ind, cur in list(enumerate(sequence))[:-1]:
            nextv = sequence[ind+1]

            conjunct+=(' (<= (+ %s %i) %s)' % (cur[0], cur[1], nextv[0]))

        disjunct+=(' (and %s)\n' % conjunct)

    f.write('(assert (or\n %s))\n' % disjunct)
nl(f)

# Max sat problem : minimize finish time
if do_maxSAT:
    f.write('(define-fun max ((x Int) (y Int)) Int (ite (< x y) y x))\n')
    nl(f)
    min_clause = ''
    i = 0
    for job in processing_times[:-1]:
        l = len(job) -1
        min_clause+=('(max (+ t%i%i %i) ' % (i, l, job[l]))
        i +=1
    l = len(processing_times[i]) - 1
    min_clause+=('(+ t%i%i %i)' % (i,l, processing_times[i][l]))
    for job in processing_times[:-1]:
        min_clause+=')'

    f.write('(minimize %s)\n' % min_clause)
    f.write('(check-sat)\n(get-model)')
else:

    f.write('(check-sat)\n(get-model)')

nl(f)
f.close()
