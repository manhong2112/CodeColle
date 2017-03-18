(defn quicksort
  [lst]
  (cond
    (= (count lst) 0) '()
    :else
        (let [t (first lst) l (rest lst)]
          (merge
            (quicksort
              (filter
                (fn [x] (< x t))
                l))
            [t]
            (quicksort
              (filter
                (fn [x] (not (< x t)))
                l))
            ))))

(defn merge
  [& args]
  (cond
    (= (count args) 0) '()
    :else
        (cons* (first args) (apply merge (rest args)))))

(defn cons*
  [lst1 lst2]
  (cond
    (= (count lst1) 0) lst2
    :else (cons (first lst1) (cons* (rest lst1) lst2))))

(defn random-list
  [n]
  (cond
    (= n 0) '()
    :else 
        (cons 
            (rand-int 
                (int (/ 
                        (abs (* (+ n 1) (+ n 2) (+ n 3)))
                        (let [x (abs (* (- n 1)))]
                            (if (= x 0) 1 x)))))
            (random-list (- n 1)))))