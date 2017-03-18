#lang racket
(define ext-env
  (lambda (x v env)
    (cons `(,x . ,v) env)))
    
(define lookup
  (lambda (x map)
    (cond
      [(eq? x (car (car map))) (cdr (car map))]
      [else (lookup x (cdr map))])))

(struct Closure (f env))

(define interp1
  (lambda (exp env)
    (match exp
      [(? symbol? x) (lookup x env)]
      [(? number? x) x]
      [`(lambda (,x) ,e) (Closure exp env)]
      [`(if ,b ,t ,f)
       (if (interp1 e env)
         (interp1 t env)
         (interp1 f env))]
      [`(let (,x ,v) ,e)
       (interp1 e (ext-env x (interp1 v env) env))]
      [`(,e1 ,e2)
       (let ([v1 (interp1 e1 env)] [v2 (interp1 e2 env)])
         (match v1
           [(Closure `(lambda (,x) ,e) env1) (interp1 e (ext-env x v2 env1))]))]
      [`(,op ,e1 ,e2)
       (let ([v1 (interp1 e1 env)] [v2 (interp1 e2 env)])
         (match op
           ['+ (+ v1 v2)]
           ['- (- v1 v2)]
           ['* (* v1 v2)]
           ['/ (/ v1 v2)]
           ['^ (expt v1 v2)]
           ['= (if (eq? v1 v2) '#T '#F)]))])))

(define interp (lambda (exp) (interp1 exp '())))