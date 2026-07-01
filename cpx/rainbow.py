import board
import supervisor
import gc
import neopixel
from adafruit_led_animation.color import RED, GREEN, BLUE, PINK, TEAL, YELLOW, WHITE, PURPLE, ORANGE


pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03, auto_write=False)

def make_state(idx):
    gc.collect()  # reclaim previous state's memory before allocating new one

    if idx == 0:
        from adafruit_led_animation.animation.rainbow import Rainbow
        return Rainbow(pixels, speed=0.05, period=2)
    if idx == 1:
        from adafruit_led_animation.animation.rainbowchase import RainbowChase
        return RainbowChase(pixels, speed=0.05, size=3, spacing=2)
    if idx == 2:
        from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
        return RainbowSparkle(pixels, speed=0.05, num_sparkles=3)
    if idx == 3:
        from adafruit_led_animation.animation.rainbowcomet import RainbowComet
        return RainbowComet(pixels, speed=0.05, tail_length=7, bounce=True)
    #Cool - bouncing rainbow comet
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