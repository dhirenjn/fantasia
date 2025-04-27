# Write your code here :-)
from machine import Pin, PWM, TouchPad
import time

# --- LED Setup ---
led_pins = [32, 5, 18, 19, 23]  # LED1–LED5 (now all flicker)
led_pwms = [PWM(Pin(p), freq=200, duty=0) for p in led_pins]

# Flicker sequence
duty_seq = [
    128, 800, 128, 800, 128, 800, 128,
    800, 800, 800,
    128, 800, 128, 800, 128, 800, 128,
    33, 33, 64
]
step_delay = 0.1

# --- Touch Pin Configuration ---
# GPIO : (threshold, frequency, led_index)
touch_configs = {
    4:  (300, 262, 0),   # Sa → LED1
    12: (300, 294, 1),   # Re → LED2
    15: (300, 330, 2),   # Ga → LED3
    13: (300, 349, 3),   # Ma → LED4
    14: (300, 392, 4),   # Pa → LED5
}

# Initialize touchpads
touch_pads = {}
for gpio, (thresh, freq, led_idx) in touch_configs.items():
    try:
        tp = TouchPad(Pin(gpio))
        tp.config(thresh)
        _ = tp.read()  # test read
        touch_pads[gpio] = {
            'tp': tp,
            'threshold': thresh,
            'freq': freq,
            'led_idx': led_idx
        }
        print(f"[OK] TouchPad GPIO{gpio} → LED{led_idx + 1}")
    except Exception as e:
        print(f"[SKIP] GPIO{gpio} not usable as TouchPad: {e}")

# --- Speaker Setup ---
speaker = PWM(Pin(25), freq=262, duty=0)

# --- Flicker sequence tracker ---
seq_pos = [0] * len(led_pwms)

print("Ready. Touch to play notes and flicker LEDs.")

while True:
    touched = []

    # Detect touch
    for cfg in touch_pads.values():
        if cfg['tp'].read() < cfg['threshold']:
            touched.append(cfg)

    # Speaker: highest freq wins
    if touched:
        top = max(touched, key=lambda c: c['freq'])
        speaker.freq(top['freq'])
        speaker.duty(512)
    else:
        speaker.duty(0)

    # LED flickering (independent)
    for i in range(len(led_pwms)):
        active = any(cfg['led_idx'] == i for cfg in touched)
        if active:
            led_pwms[i].duty(duty_seq[seq_pos[i]])
            seq_pos[i] = (seq_pos[i] + 1) % len(duty_seq)
        else:
            led_pwms[i].duty(0)
            seq_pos[i] = 0

    time.sleep(step_delay)
