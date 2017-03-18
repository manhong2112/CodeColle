#lang racket
(def mytrue (fn [t f] t))
(def myfalse (fn [t f] f))
(def myif (fn [b t f] (b t f)))
(def myor (fn [b1 b2] (myif b1 mytrue b2)))
(def myand (fn [b1 b2] (myif b1 b2 myfalse)))
(def mynot (fn [b] (myif b myfalse mytrue)))
(def myxor (fn [b1 b2] (myif b1 (mynot b2) b2)))

