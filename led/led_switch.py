#!/usr/bin/env python

from gpiozero import LED, Button
from signal import pause

LED_GPIO_PIN = 17
BUTTON_GPIO_PIN = 2

def main():
    led = LED(LED_GPIO_PIN)
    button = Button(BUTTON_GPIO_PIN)

    while True:
        button.when_pressed = led.on
        button.when_released = led.off

        pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminating...")
