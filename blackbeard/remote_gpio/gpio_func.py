from gpiozero import LED
from time import sleep
import numpy as np


def turn_led_on(pin=None, blink=1):
    """ Turn on and off specific LED
    :param pin: GPIO pin number the LED is connected to
    :param blink: Number of times the led should blink
    :return: LED Blinking
    """
    led = LED(pin)

    try:

        for i in np.arange(blink):
            led.on()
            print(f"LED with pin {pin} turned on.")
            sleep(1)
            led.off()
            print(f"LED with pin {pin} turned off.")

    finally:
        sleep(1)


def temp_text_on_pi_display(text="temporary hello", seconds=3):
    """ Display text temporary on Raspberry Pi
    :param text: text that should be displayed
    :param seconds: number of seconds the text should stay displayed
    :return: Display temporary text
    """
    text = ...


def perm_text_on_pi_display(text="hello"):
    """ Display text permanently on Raspberry Pi
    :param text: text that should be displayed
    :return: Display permanent text
    """
    text = ...


def display_card_count(counter):
    ...


def display_card_detected(detected_cards):
    ...

