;; key=value | key=[true]
(define (str-split str ch maxn)
  (let ((len (string-length str)))
    (letrec
      [(split (lambda (a b n)
               (cond
                  [(= maxn 0) (cons str '())]
                  [(>= b len) (if (= a b) '() (cons (substring str a b) '()))]
                  [(= maxn n) (cons (substring str (+ 1 b) len) '())]
                  [(char=? ch (string-ref str b))
                   (if (= a b)
                      (split (+ 1 a) (+ 1 b) n)
                      (cons (substring str a b) (split b b (+ n 1))))]
                  [else (split a (+ 1 b) n)])))]
      (split 0 0 0))))

(define (str-elem? str ch)
   (let ([len (string-length str)])
        (letrec ([f (lambda (n)
                        (cond [(>= n len) #f]
                              [(char=? ch (string-ref str n)) #t]
                              [else (f (+ n 1))]))])
           (f 0))))

(define (list->pair lst)
   (letrec ([f (case-lambda
                  [() '()]
                  [(x y . rest) (cons (cons x y) (apply f rest))]
                  [(x . rest) (cons (cons '() x) (apply f rest))])])
           (apply f lst)))


(define (string-parse str)
  (case (string-downcase str)
    [("true" "#t") #t]
    [("false" "#f") #f]
    [else str]))

(define args-parse
   (lambda (args)
      (map (lambda (arg)
              (if (str-elem? arg #\=)
                (let* ([args0 (car (list->pair (str-split arg #\= 1)))]
                       [key (car args0)]
                       [value (string-parse (cdr args0))])
                      (cons key value))
                (cons arg #t)))
         args)))
