from machine import Pin, PWM
import random
from utime import ticks_us, ticks_diff, ticks_add, sleep_ms, sleep_us

random.seed(ticks_us())

# global constants
MAX_DUTY = 0xFFFF // 2
TICKS_MAX = 0x3FFFFFFF          # may be useful later? 30 bits
TEMP_F0_DUTY = MAX_DUTY
FUNDAMENTAL = 108                # Freq in Hz

PIN_F0 = 0
PIN_F1 = 2
PIN_F2 = 4


# initializes a vowel sound
# 
# f1: formant 1 frequency in hertz, integer
# f2: formant 2 frequency in hertz, integer
# f2_db: relative db to f1, integer
# name: string descriptor
# f0_duty: temporarily set to 10k, 16 bit value of duty cycle of the fundamental
class VowelMonophone:
    def __init__(self, f1, f2, f2_db, name, f0_duty=TEMP_F0_DUTY ):

        self.f0_freq = FUNDAMENTAL
        self.f1_freq = f1
        self.f2_freq = f2

        self.f0_duty = f0_duty
        self.f1_duty = MAX_DUTY
        self.f2_duty = (int((10 ** (f2_db / 20)) * MAX_DUTY)) & 0xFFFF

        self.name = name

class PhoneStore:
    def __init__(self):

        # Define monophones
        # f0_duty may be added later if issues crop up
        self.vowel_monophones = [

            VowelMonophone(270, 2290, -16, "EE"), # /i/
            VowelMonophone(390, 1990, -12, "IH"), # /I/
            VowelMonophone(530, 1840, -9,  "EH"), # /ɛ/
            VowelMonophone(660, 1720, -7,  "AE"), # /æ/
            VowelMonophone(730, 1090, -4,  "AH"), # /a/
            VowelMonophone(570, 840,  -5,  "AW"), # /ɔ/
            VowelMonophone(440, 1020, -11, "OU"), # /ʊ/
            VowelMonophone(300, 870,  -15, "OO"), # /u/
            VowelMonophone(520, 1190, -8,  "UH"), # /ʌ/
            VowelMonophone(500, 1500, -6,  "UA")  # /ə/

        ]

class VowelPlayer:
    def __init__(self):
        self.vm = PhoneStore().vowel_monophones
        self.vmi = 0
        self.vm_next = 0

        # init pins
        self.pin_f0 = Pin(PIN_F0, Pin.OUT)
        self.pin_f1 = Pin(PIN_F1, Pin.OUT)
        self.pin_f2 = Pin(PIN_F2, Pin.OUT)

        # init PWM with 0 duty (no volume at init)
        self.pwm_f0 = PWM(self.pin_f0, freq=FUNDAMENTAL, duty_u16=0)
        self.pwm_f1 = PWM(self.pin_f1, freq=self.vm[self.vmi].f1_freq, duty_u16=0)
        self.pwm_f2 = PWM(self.pin_f2, freq=self.vm[self.vmi].f2_freq, duty_u16=0)
        

        self.pins = [self.pwm_f0, self.pwm_f1, self.pwm_f2]

        self.s_curve = [1, 1, 1, 1, 1, 
                        2, 2, 2, 2, 
                        3, 3, 
                        4, 
                        3, 3, 
                        2, 2, 2, 2, 
                        1, 1, 1, 1, 1]
        
        self.s_curve_sum = 0
        for i in self.s_curve:
            self.s_curve_sum += i
        self.curve_steps = len(self.s_curve)

    def update_duty(self, pin, amt):
        duty = pin.duty_u16()
        pin.duty_u16(duty + amt)

    def update_freq(self, pin, amt):
        freq = pin.freq()
        pin.freq(freq + amt)

    def set_freq(self, pin, freq):
        pin.freq(freq)

    def init_playback(self):
        self.update_duty(self.pwm_f0, self.vm[self.vmi].f0_duty)
        self.update_duty(self.pwm_f1, self.vm[self.vmi].f1_duty)
        self.update_duty(self.pwm_f2, self.vm[self.vmi].f2_duty)

    def test_all(self):
        count = 0
        for i in self.vm:

            
            self.pwm_f0.duty_u16(i.f0_duty)

            self.pwm_f1.freq(i.f1_freq)
            self.pwm_f1.duty_u16(i.f1_duty)

            self.pwm_f2.freq(i.f2_freq)
            self.pwm_f2.duty_u16(i.f2_duty)

            print(i.name)

            sleep_ms(1100)

            count += 1
            count = count % len(self.vm)

            goal_f_f1 = self.vm[count].f1_freq
            goal_f_f2 = self.vm[count].f2_freq
            goal_d_f2 = self.vm[count].f2_duty

            f_f1_step = int((goal_f_f1 - i.f1_freq) / self.s_curve_sum)
            f_f2_step = int((goal_f_f2 - i.f2_freq) / self.s_curve_sum)
            d_f2_step = int((goal_d_f2 - i.f2_duty) / self.s_curve_sum)

            for j in range(len(self.s_curve)):
                
                self.update_freq(self.pwm_f1, f_f1_step * self.s_curve[j])
                self.update_freq(self.pwm_f2, f_f2_step * self.s_curve[j])
                self.update_duty(self.pwm_f2, d_f2_step * self.s_curve[j])
                sleep_ms(3)


def main():
    player = VowelPlayer()
    player.test_all()
    

main()
        



        


    
