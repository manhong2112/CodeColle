

(define Y (lambda (f) ((lambda (u) (u u)) (lambda (F) (f (lambda (v) ((F F) v)))))))

((Y (lambda (f) (lambda (x) (if (= x 0) 1 (* x (f (- x 1))))))) 5)

((((lambda (f) ((lambda (u) (u u)) (lambda (F) (f (lambda (v) ((F F) v))))))
   (lambda (_F)
     (lambda (_x)
       (lambda (_val)
         (if (= _x 0) _val ((_F (- _x 1)) (* _val _x))))))) 5) 1)

(let ((F (lambda (f) (lambda (x) (if (= x 0) 1 (* x (f (- x 1)))))))) ((Y F) 5))

(define value (lambda (x)
               (cond ((number? x) x)
                 (else (let ([v1 (value (second x))] [v2 (value (third  x))])
                        (case (first x)
                          ['+ (+ v1 v2)]
                          ['- (- v1 v2)]
                          ['* (* v1 v2)]
                          ['/ (/ v1 v2)]
                          ['^ (expt v1 v2)]))))))

(define first (lambda (x) (car x)))
(define second (lambda (x) (car (cdr x))))
(define third (lambda (x) (car (cdr (cdr x)))))

(display (let
          ((Y (lambda (f) ((lambda (u) (u u)) (lambda (F) (f (lambda (v) ((F F) v))))))))
          (let
            ((F (lambda (f) (lambda (x) (if (= x 0) 1 (* x (f (- x 1))))))))
            ((Y F) 10000))))
