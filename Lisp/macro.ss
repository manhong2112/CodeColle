(define-syntax 如果
  (syntax-rules ()
    ((如果 b t f) (if b t f))))