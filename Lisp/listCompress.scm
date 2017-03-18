(define (compress lst)
    (compress0 (car lst) 1 (cdr lst) '())
)

(define (compress0 ele n lst res)
    (cond 
        [(null? lst)
            (if (= n 1)
                `(,ele . ,res)
                `((,ele . ,n) . ,res)
            )]
        [(eq? ele (car lst))
            (compress0 ele (+ n 1) (cdr lst) res)]
        [else
            (compress0 (car lst) 1 (cdr lst) 
                (if (= n 1)
                    `(,ele . ,res)
                    `((,ele . ,n) . ,res)
                ))
        ]))

(define (decompress lst)
    (cond
        [(null? lst) '()]
        [(atom? (car lst))
            (cons (car lst) (decompress (cdr lst)))]
        [else
            (repeat (car (car lst)) (cdr (car lst)) (decompress (cdr lst)))]
    )
)

(define (repeat ele time lst)
    (cond
        [(= time 0) lst]
        [else (repeat ele (- time 1) (append lst `(,ele)))]))