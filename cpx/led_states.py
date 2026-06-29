import sys
import board
import supervisor
import gc
import neopixel
from adafruit_led_animation.color import RED, GREEN, BLUE, PINK, TEAL, YELLOW, WHITE, PURPLE, ORANGE



pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.03, auto_write=False)

def make_state(idx):
    #THe last lines under, of gc.collect to gc.collect() broke the code.
    gc.collect()
    for mod_name in list(sys.modules):
        if mod_name.startswith("adafruit_led_animation.animation"):
            del sys.modules[mod_name]


    gc.collect()  # reclaim previous state's memory before allocating new one
    if idx == 0:
        from adafruit_led_animation.animation.pulse import Pulse
        return Pulse(pixels, speed=0.05, color=BLUE, period=3)
    if idx == 1:
        from adafruit_led_animation.animation.comet import Comet
        return Comet(pixels, speed=0.05, color=GREEN, tail_length=4)
    if idx == 2:
        from adafruit_led_animation.animation.blink import Blink
        return Blink(pixels, speed=0.5, color=RED)
    if idx == 3:
        from adafruit_led_animation.animation.rainbow import Rainbow
        return Rainbow(pixels, speed=0.05, period=2)
    if idx == 4:
        from adafruit_led_animation.animation.rainbowchase import RainbowChase
        return RainbowChase(pixels, speed=0.05, size=3, spacing=2)
    if idx == 5:
        from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
        return RainbowSparkle(pixels, speed=0.05, num_sparkles=3)



    return None

current = make_state(0)
print("States: 0=Pulse 1=Comet 2=Blink 3=Rainbow 4=RainbowChase 5=RainbowSparkle 6=SparklePulse 7=Sparkle 8=RainbowComet 9=Chase 10=ColorCycle 11=Solid 12=CustomColorChase 13=CustomColorWipe 14=CustomColorPulse 15=CustomColorFade 16=CustomColorBreath 17=CustomColorStrobe 18=CustomColorWave 19=CustomColorChase 20=PacMan 21=Blink(Pink)")

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