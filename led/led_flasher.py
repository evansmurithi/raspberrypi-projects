#!/usr/bin/env python

from gpiozero import LED
from time import sleep

GPIO_PIN = 17

def main():
    led = LED(GPIO_PIN)

    while True:
        led.on()
        sleep(0.25)
        led.off()
        sleep(0.25)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminating...")
