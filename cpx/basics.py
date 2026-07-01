import board
import supervisor
import gc
import neopixel
from adafruit_led_animation.color import RED, GREEN, BLUE, PINK, TEAL, YELLOW, WHITE, PURPLE, ORANGE


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03, auto_write=False)

def make_state(idx):
    gc.collect()  # reclaim previous state's memory before allocating new one
    if idx == 0:
        from adafruit_led_animation.animation.pulse import Pulse
        return Pulse(pixels, speed=0.05, color=BLUE, period=3)
    if idx == 1:
        from adafruit_led_animation.animation.comet import Comet
        return Comet(pixels, speed=0.05, color=GREEN, tail_length=4)
    # Comet would be great of a loading state
    if idx == 2:
        from adafruit_led_animation.animation.blink import Blink
        return Blink(pixels, speed=0.5, color=RED)
    if idx == 3:
        from adafruit_led_animation.animation.chase import Chase
        return Chase(pixels, speed=0.05, color=GREEN, size=3, spacing=2)
    # looks like an arcade
    if idx == 4:
        from adafruit_led_animation.animation.solid import Solid
        return Solid(pixels, color=TEAL)
    if idx == 5:
        from adafruit_led_animation.animation.blink import Blink
        return Blink(pixels, speed=0.5, color=PINK, background_color=TEAL)
        # Blink between colors

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