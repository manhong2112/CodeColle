
(define d/dx
  (lambda (expr) 
    (match expr
      [(? number? x) 0]
      ['n 0] ;; assume n is number
      [(or 'e 'pi 'π) 0] ;; process const
      ['x 1] ;; assert x is the var

      ;; negative number
      [`(- ,e) (d/dx `(* -1 ,e))]

      ;; log / ln
      [`(ln x) `(/ 1 x)]
      [`(ln ,e) `(* ,(d/dx e) (^ ,e -1))]
      [`(log ,b ,x) (d/dx `(* (ln ,x) (^ (ln ,b) -1)))]

      ;; derivative
      [`(+ ,e1 ,e2) `(+ ,(d/dx e1) ,(d/dx e2))] ;; Sum Rule
      [`(- ,e1 ,e2) `(- ,(d/dx e1) ,(d/dx e2))] ;; Difference Rule
      [`(* ,e1 ,e2) `(+ (* ,(d/dx e1) ,e2) (* ,e1 ,(d/dx e2)))] ;; Product Rule
      [`(/ ,e1 ,e2) (d/dx `(* ,e1 (^ ,e2 -1)))] ;; 1/x => x^-1
      [`(^ ,e1 ,e2) `(* ,expr ,(d/dx `(* ,e2 (ln ,e1))))] ;; Power Rule

      ;; Chain Rule & special function
      [`(,f ,e) `(* ,(d0 `(,f x) e) ,(d/dx e))]
    )))

(define d0
  (lambda (expr y)
    (match expr
      [`(sin x) `(cos ,y)]
      [`(cos x) `(- (sin ,y))]
      [`(tan x) `(^ (sec ,y) 2)]
      [`(csc x) `(* (cot ,y) (csc ,y))]
      [`(sec x) `(- (* (tan ,y) (sec ,y)))]
      [`(cot x) `(- (^ (csc ,y) 2))]
    )))

(define merge
  (lambda (expr)
    (match expr
      [`(^ (^ ,n ,e1) ,e2) (merge `(^ ,n ,(merge `(* ,e1 ,e2))))]
      [`(^ ,n ,e) `(^ ,n ,(merge e))]
      [`(ln ,e) `(ln ,(merge e))]
      [`(,sym ,e1 ,e2) (merge0 sym (merge e1) (merge e2))]
      [_ expr])))

(define (merge0 sym e1 e2)
  (cond
    [(and (atom? e1) (atom? e2)) `(,sym ,e1 ,e2)]
    [(and (atom? e1) (eq? (car e2) sym)) (cons sym (cons e1 (cdr e2)))]
    [(and (atom? e2) (eq? (car e1) sym)) (cons sym (cons e2 (cdr e1)))]
    
    [(and (list? e1) (list? e2) (eq? (car e1) sym) (eq? (car e2) sym)) (cons sym (merge-list (cdr e1) (cdr e2)))]
    [(and (list? e1) (eq? (car e1) sym)) (cons sym (cons e2 (cdr e1)))]
    [(and (list? e2) (eq? (car e2) sym)) (cons sym (cons e1 (cdr e2)))]

    [else `(,sym ,e1 ,e2)]))

(define (merge-list lst1 lst2)
  (cond ((null? lst1) lst2)
        ((null? lst2) lst1)
        ((atom? lst1) (cons lst1 lst2))
        ((atom? lst2) (cons lst2 lst1))
        (else (cons (car lst1)
                    (merge-list lst2 (cdr lst1))))))

(define atom? (lambda (x) (or (symbol? x) (number? x))))

(define prefix2infix 
  (lambda (expr)
    (match expr
      [(? atom? x) expr]
      [`(log ,b ,e) `(log ,(prefix2infix b) ,(prefix2infix e))]
      [`(,f ,e) `(,f ,(prefix2infix e))]
      [`(,sym ,e1 ,e2) `(,(prefix2infix e1) ,sym ,(prefix2infix e2))]
    )
  ))