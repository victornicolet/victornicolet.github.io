(declare-const t00 Int)
(declare-const t01 Int)
(declare-const t02 Int)
(declare-const t10 Int)
(declare-const t11 Int)
(declare-const t12 Int)
(declare-const t20 Int)
(declare-const t21 Int)

;; Start times are positive
(assert (and (>= t00 0) (>= t01 0) (>= t02 0)
	     (>= t10 0) (>= t11 0) (>= t12 0)
	     (>= t20 0) (>= t21 0)))

;; Each task in the job will be executed ater the preivous has been completed
;; job 0 = [(0, 3), (1, 2), (2, 2)]
;; job 1 = [(0, 2), (2, 1), (1, 4)]
;; job 2 = [(1, 4), (2, 3)]

(assert (and (>= (+ t01 3) t00) (>= (+ t02 2) t01)))
(assert (and (>= (+ t11 2) t10) (>= (+ t12 1) t11)))
(assert (>= (+ t21 4) t20))

;; Each machine can only work on one job at a time
;; Machine 2
(assert (or (>= (+ t02 2) t21) (>= (+ t21 3) t02)))
;; Machine 1 : t20, t01, t12
(assert (or (and (>= ()))))
(check-sat)
(get-model)
