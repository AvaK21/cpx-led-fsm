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