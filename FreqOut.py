from machine import Pin, PWM
import random
from utime import ticks_us

random.seed(ticks_us())

INTERP_FORM_MIN_US = 5_000
INTERP_FORM_MAX_US = 60_000

class FreqOut:

    def __init__(self, out_pin, freq_floor, freq_ceil):

        self.freq = random.randint(freq_floor, freq_ceil)
        self.start = ticks_us()

        self.pwm_pin = Pin(out_pin, Pin.OUT)
        self.pwm_output = PWM(self.pwm_pin,                                                   
                              freq=self.freq,                                                   
                              duty_u16=0)



def main():

    freq0 = FreqOut(0, 100, 250)
    freq1 = FreqOut(2, 600, 1400)
    freq2 = FreqOut(4, 2500, 3000)

    freqs = [freq0, freq1, freq2]

