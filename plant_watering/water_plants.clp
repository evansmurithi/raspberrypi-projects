; facts:
;   soil-has-moisture yes/no
;   temperature-is high/low
;   humidity-is high/low
;   time-of-day-is morning/mid-morning/afternoon/evening/night

(defrule plant-needs-water-high-temperatures
    (humidity-is high)
    (temperature-is high)
    (time-of-day-is mid-morning|afternoon)
=>
    (assert (plant-needs water))
)

(defrule plant-needs-water-time-of-day
    (time-of-day-is morning|evening)
=>
    (assert (plant-needs water))
)

(defrule water-plant-soil-moisture
    (soil-has-moisture yes)
    (plant-needs water)
=>
    (assert (water-plant no))
    (printout t "Don't water plant" crlf)
)

(defrule water-plant-soil-no-moisture
    (soil-has-moisture no)
    (plant-needs water)
=>
    (assert (water-plant yes))
    (printout t "Water plant" crlf)
)
