import board
import supervisor
import gc
import neopixel
from adafruit_led_animation.color import RED, GREEN, BLUE, PINK, TEAL, YELLOW, WHITE, PURPLE, ORANGE

# only tested the first one
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03, auto_write=False)

def make_state(idx):
    gc.collect()  # reclaim previous state's memory before allocating new one

    if idx == 0:
        from adafruit_led_animation.animation.customcolorchase import CustomColorChase
        return CustomColorChase(pixels, speed=0.05, colors=[YELLOW, PURPLE, ORANGE], size=3, spacing=2)



    return None

current = make_state(0)

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