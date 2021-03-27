import time
import adafruit_dht
import RPi.GPIO as GPIO
import RTC_DS1302
import os


class InputDevice:

    def get_value(self):
        raise NotImplementedError()

    def cleanup(self):
        raise NotImplementedError()


class TempHumiditySensor(InputDevice):

    def __init__(self, gpio_pin):
        self.dht_device = adafruit_dht.DHT11(gpio_pin)

    def get_value(self):
        while True:
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity
                break
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2)
                continue
            except Exception as error:
                self.dht_device.exit()
                raise error

        return {
            'temperature': temperature,
            'humidity': humidity,
        }

    def cleanup(self):
        self.dht_device.exit()


class SoilMoistureSensor(InputDevice):

    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN)

    def get_value(self):
        return {
            'moisture': GPIO.input(self.gpio_pin) == 0,
        }

    def cleanup(self):
        GPIO.cleanup()


class RTCModule(InputDevice):

    def __init__(self):
        self.rtc = RTC_DS1302.RTC_DS1302()
        date_string = os.popen('date +"%y %m %d %u %H %M %S"').read()
        self.rtc.WriteRAM('Last set: ' + os.popen('date +"%Y-%m-%d %H:%M:%S"').read().replace("\n", ""))
        date_array = date_string.split()
        self.rtc.WriteDateTime(
            int(date_array[0]),
            int(date_array[1]),
            int(date_array[2]),
            int(date_array[3]),
            int(date_array[4]),
            int(date_array[5]),
            int(date_array[6])
        )

    def get_value(self):
        date_time = {
            "Year": 0,
            "Month": 0,
            "Day": 0,
            "Hour": 0,
            "Minute": 0,
            "Second": 0
        }
        data = self.rtc.ReadDateTime(date_time)
        return {
            'datetime': date_time,
        }

    def cleanup(self):
        self.rtc.CloseGPIO()


class OutputDevice:

    def output(self, **kwargs):
        raise NotImplementedError()


class LCD(OutputDevice):

    def output(self, **kwargs):
        pass


class Buzzer(OutputDevice):

    def output(self, **kwargs):
        pass
