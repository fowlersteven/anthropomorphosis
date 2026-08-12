from machine import Pin, PWM
import random
from utime import ticks_us

random.seed(ticks_us())

INTERP_FORM_MIN_US = 5_000
INTERP_FORM_MAX_US = 60_000

class FreqOut:

    def __init__(self, out_pin, freq_floor, freq_ceil
                 duty_floor, duty_ceil):
        
        self.dfloor = duty_floor
        self.dceil = duty_ceil         
        self.ffloor = freq_floor
        self.fceil = freq_ceil
        self.freq = random.randint(self.ffloor, self.fceil)
        self.start = ticks_us()
        self.duty = random.randint(self.dfloor, dceil)
        self.pwm_pin = Pin(out_pin, Pin.OUT)
        self.pwm_output = PWM(self.pwm_pin,
                              freq=self.freq,
                              duty_u16=self.duty)

    def genAttr(self):
        self.freq = random.randint(self.ffloor, self.fceil)
        self.duty = random.randint(self.dfloor, self.dceil)
    def getFreq(self):
        return self.freq
    def getDuty(self):
        return self.duty
    def interpolate(self, timestep_us):
        if ticks_diff(ticks_add(timestep_us, self.start), ticks_us()) <= 0:
            pass
            
class TimeController:
    def __init__(self):
        pass
        

def main():

    freq0 = FreqOut(0, 100, 250)
    freq1 = FreqOut(2, 600, 1400)
    freq2 = FreqOut(4, 2500, 3000)

    freqs = [freq0, freq1, freq2]
    
