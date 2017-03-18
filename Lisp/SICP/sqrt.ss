(define root
    (lambda (x p)
        (root0 x
               p
               (/ x (/ p 1.0)))))

(define root0
    (lambda (x p t)
        (let
            [(n_t (/ x (pow t (- p 1))))]
            (if (= n_t t)
                n_t
                (root0 x p 
                    (/ (+ (/ x (pow t
                                    (- p 1)))
                          (* t (- p 1)))
                       p))
            )
        )
    )
)

(define abs
    (lambda (x) (if (< x 0) -x x)))

(define pow 
    (lambda (x p) 
        (if (= p 0)
            1
            (* x (pow x (- p 1))))))
(display (root 25 3))
(exit)