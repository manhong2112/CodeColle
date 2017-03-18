(define (append lat x)
        (cond
            [(null? lat) (cons x '())]
            [else
                (cons
                    (car lat)
                    (append (cdr lat) x))]))
(define (last lat)
    (cond
        [(null? (cdr lat)) (car lat)]
        [else (last (cdr lat))]))

(define (sum-prefix lat) (sum-prefix-b (cdr lat) (cons (car lat) '())))
(define (sum-prefix-b lat collector)
    (cond
        [(null? lat) 
            collector]
        [else 
            (sum-prefix-b
               (cdr lat)
               (append
                    collector
                    (+ 
                        (last collector)
                        (car lat))))]))

(display (sum-prefix '(1 2 3 4 5 6 7 8 9 10)))
(exit)