# Write your code here :-)
from machine import Pin, PWM, TouchPad
import time

led1 = PWM(Pin(32))
led2 = PWM(Pin(5))
led3 = PWM(Pin(18))
led4 = PWM(Pin(19))
led5 = PWM(Pin(23))

led1.freq(200)
led2.freq(200)
led3.freq(200)
led4.freq(200)
led5.freq(200)

led1.duty(0)
led2.duty(0)
led3.duty(0)
led4.duty(0)
led5.duty(0)

leds = [led1, led2, led3, led4, led5]

duty_seq = [
    128, 800, 128, 800, 128, 800, 128,
    800, 800, 800,
    128, 800, 128, 800, 128, 800, 128,
    33, 33, 64
]

seq_pos = [0, 0, 0, 0, 0]

touch1 = TouchPad(Pin(4))
touch2 = TouchPad(Pin(12))
touch3 = TouchPad(Pin(15))
touch4 = TouchPad(Pin(13))
touch5 = TouchPad(Pin(14))

touch1.config(300)
touch2.config(300)
touch3.config(300)
touch4.config(300)
touch5.config(300)

touchpads = [touch1, touch2, touch3, touch4, touch5]
freqs = [262, 294, 330, 349, 392]

speaker = PWM(Pin(25))
speaker.freq(262)
speaker.duty(0)

while True:
    touched = []

    if touch1.read() < 300:
        touched.append((262, 0))
    if touch2.read() < 300:
        touched.append((294, 1))
    if touch3.read() < 300:
        touched.append((330, 2))
    if touch4.read() < 300:
        touched.append((349, 3))
    if touch5.read() < 300:
        touched.append((392, 4))

    if touched:
        top = max(touched, key=lambda x: x[0])
        speaker.freq(top[0])
        speaker.duty(512)
    else:
        speaker.duty(0)

    for i in range(5):
        active = False
        for freq, idx in touched:
            if idx == i:
                active = True
        if active:
            leds[i].duty(duty_seq[seq_pos[i]])
            seq_pos[i] = (seq_pos[i] + 1) % len(duty_seq)
        else:
            leds[i].duty(0)
            seq_pos[i] = 0

    time.sleep(0.1)
