(declare-const t00 Int)
(declare-const t01 Int)
(declare-const t02 Int)
(declare-const t10 Int)
(declare-const t11 Int)
(declare-const t12 Int)
(declare-const t20 Int)
(declare-const t21 Int)

(assert (and (>= t00 0) (>= t01 0) (>= t02 0) (>= t10 0) (>= t11 0) (>= t12 0) (>= t20 0) (>= t21 0)))

(assert (and (<= (+ t00 3)  t01) (<= (+ t01 2)  t02)))
(assert (and (<= (+ t10 2)  t11) (<= (+ t11 1)  t12)))
(assert (and (<= (+ t20 4)  t21)))

(assert (or
  (and  (<= (+ t00 3) t10))
 (and  (<= (+ t10 2) t00))
))
(assert (or
  (and  (<= (+ t01 2) t12) (<= (+ t12 4) t20))
 (and  (<= (+ t01 2) t20) (<= (+ t20 4) t12))
 (and  (<= (+ t12 4) t01) (<= (+ t01 2) t20))
 (and  (<= (+ t12 4) t20) (<= (+ t20 4) t01))
 (and  (<= (+ t20 4) t01) (<= (+ t01 2) t12))
 (and  (<= (+ t20 4) t12) (<= (+ t12 4) t01))
))
(assert (or
  (and  (<= (+ t02 2) t11) (<= (+ t11 1) t21))
 (and  (<= (+ t02 2) t21) (<= (+ t21 3) t11))
 (and  (<= (+ t11 1) t02) (<= (+ t02 2) t21))
 (and  (<= (+ t11 1) t21) (<= (+ t21 3) t02))
 (and  (<= (+ t21 3) t02) (<= (+ t02 2) t11))
 (and  (<= (+ t21 3) t11) (<= (+ t11 1) t02))
))

(define-fun max ((x Int) (y Int)) Int (ite (< x y) y x))

(minimize (max (+ t02 2) (max (+ t12 4) (+ t21 3))))
(check-sat)
(get-model)
