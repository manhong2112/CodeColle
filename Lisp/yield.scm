(define yield (lambda (f)
                (lambda (x) 
                    (cons (car x) (lambda () ((yield f) (f x)))))))