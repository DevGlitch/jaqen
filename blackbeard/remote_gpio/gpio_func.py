from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button, LED
from time import sleep
import numpy as np


def connect_remote_gpio(host_ip):
    """ Connect to remote GPIO host
    :param host_ip: IP address of your raspberry pi
    :return: factory object
    """
    factory = PiGPIOFactory(host=host_ip)
    return factory


def turn_led_on_off(pin, factory, blink, time_on=0.5, time_off=1):
    """ Turn on and off specific LED
    :param pin: GPIO pin number the LED is connected to
    :param factory: PiGPIOFactory Host
    :param blink: Number of times the led should blink
    :param time_on: Seconds the led should stay
    :param time_off: Seconds the led should stay
    :return: LED Blinking
    """
    led = LED(pin, pin_factory=factory)

    for i in np.arange(blink):
        led.on()
        print(f"LED at pin {pin} turned on.")
        sleep(time_on)
        led.off()
        print(f"LED at pin {pin} turned off.")
        sleep(time_off)


def button_wait_for_press(pin, factory, timeout=None):
    """ Wait for button to be pressed
    :param pin: GPIO pin number the button is connected to
    :param factory: PiGPIOFactory Host
    :param timeout: Number of seconds to wait before proceeding (None = Wait indefinitely)
    :return: Pause script until button is pressed
    """
    button = Button(pin, pin_factory=factory)
    print(f"Waiting for button at pin {pin} to be pressed.")
    button.wait_for_press(timeout)
    print(f"The button at pin {pin} was pressed.")
    return True


def button_wait_for_release(pin, factory, timeout=None):
    """ Wait for button to be released
    :param pin: GPIO pin number the button is connected to
    :param factory: PiGPIOFactory Host
    :param timeout: Number of seconds to wait before proceeding (None = Wait indefinitely)
    :return: Pause script until button is released
    """
    button = Button(pin, pin_factory=factory)
    print(f"Waiting for button at pin {pin} to be released.")
    button.wait_for_press(timeout)
    print(f"The button at pin {pin} was released.")
    return True


def button_when_pressed(pin, factory):
    """
    :param pin:
    :param factory:
    :return:
    """
    button = Button(pin, pin_factory=factory)
    button.when_pressed()
    print(f"The button at pin {pin} was pressed.")


def button_when_released(pin, factory):
    """
    :param pin:
    :param factory:
    :return:
    """
    button = Button(pin, pin_factory=factory)
    button.when_released()
    print(f"The button at pin {pin} was released.")
