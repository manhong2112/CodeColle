(define-syntax --
    (syntax-rules ()
        ((_ n) (- n 1)))
)

(define (fact n)
    (cond
        [(= n 0) 1]
        [else (* n (fact (-- n)))]
    )
)

(define Y
    (lambda (f) 
    ((lambda (u) (u u))
     (lambda (g)
        (f (lambda (x) ((g g) x))))
    ))
)

