import board
import supervisor
import gc
import neopixel
from adafruit_led_animation.color import RED, GREEN, BLUE, PINK, TEAL, YELLOW, WHITE, PURPLE, ORANGE


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03, auto_write=False)

def make_state(idx):
    gc.collect()  # reclaim previous state's memory before allocating new one

    if idx == 0:
        from adafruit_led_animation.animation.colorcycle import ColorCycle
        return ColorCycle(pixels, speed=0.05, colors=[RED, GREEN, BLUE])
#Cycles of having all the pixeled different colors.
    if idx == 1:
        from adafruit_led_animation.animation.sparkle import Sparkle
        return Sparkle(pixels, speed=1, color=PURPLE, num_sparkles=3)
# Turns on a few random pixels at a time,
    if idx == 2:
        from adafruit_led_animation.animation.sparklepulse import SparklePulse
        return SparklePulse(pixels, speed=0.05, color=BLUE, period=3)
# Turns on a few random pixels at a time, and then fades them out, and repeats this process.


    return None

current = make_state(2)

while True:
    if supervisor.runtime.serial_bytes_available:
        try:
            idx = int(input())
            new_state = make_state(idx)
            if new_state:
                current = new_state
                print(f"State {idx} | free: {gc.mem_free()}")
            else:
                print(f"No state {idx}")
        except ValueError:
            print("Enter an integer")
    current.animate()