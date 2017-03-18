#lang racket
(define tree-sum (lambda (tree) 
    (cond 
        [(number? tree) tree]
        [else (+ (tree-sum (car tree)) (tree-sum (car (cdr tree))))])))