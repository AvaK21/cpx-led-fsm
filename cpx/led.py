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
    if idx == 6:
        from adafruit_led_animation.animation.sparklepulse import SparklePulse
        return SparklePulse(pixels, speed=0.05, color=PINK, period=3)
    if idx == 7:
        from adafruit_led_animation.animation.sparkle import Sparkle
        return Sparkle(pixels, speed=0.05, color=RED, num_sparkles=3)
    if idx == 8:
        from adafruit_led_animation.animation.rainbowcomet import RainbowComet
        return RainbowComet(pixels, speed=0.05, tail_length=7, bounce=True)
    if idx == 9:
        from adafruit_led_animation.animation.chase import Chase
        return Chase(pixels, speed=0.05, color=GREEN, size=3, spacing=2)
    if idx == 10:
        from adafruit_led_animation.animation.colorcycle import ColorCycle
        return ColorCycle(pixels, speed=0.05, colors=[RED, GREEN, BLUE])
    if idx == 11:
        from adafruit_led_animation.animation.solid import Solid
        return Solid(pixels, color=TEAL)
    if idx == 12:
        from adafruit_led_animation.animation.customcolorchase import CustomColorChase
        return CustomColorChase(pixels, speed=0.05, colors=[YELLOW, PURPLE, ORANGE], size=3, spacing=2)
    if idx == 13:
        from adafruit_led_animation.animation.customcolorwipe import CustomColorWipe
        return CustomColorWipe(pixels, speed=0.05, colors=[WHITE, BLUE, RED])
    if idx == 14:
        from adafruit_led_animation.animation.customcolorpulse import CustomColorPulse
        return CustomColorPulse(pixels, speed=0.05, colors=[GREEN, ORANGE, PURPLE], period=3)
    if idx == 15:
        from adafruit_led_animation.animation.customcolorfade import CustomColorFade
        return CustomColorFade(pixels, speed=0.05, colors=[RED, GREEN, BLUE], period=3)
    if idx == 16:
        from adafruit_led_animation.animation.customcolorbreath import CustomColorBreath
        return CustomColorBreath(pixels, speed=0.05, colors=[TEAL, YELLOW, PINK], period=3)
    if idx == 17:
        from adafruit_led_animation.animation.customcolorstrobe import CustomColorStrobe
        return CustomColorStrobe(pixels, speed=0.05, colors=[WHITE, RED, BLUE], period=3)
    if idx == 18:
        from adafruit_led_animation.animation.customcolorwave import CustomColorWave
        return CustomColorWave(pixels, speed=0.05, colors=[PURPLE, ORANGE, GREEN], period=3)
    if idx == 19:
        from adafruit_led_animation.animation.customcolorchase import CustomColorChase
        return CustomColorChase(pixels, speed=0.05, colors=[RED, GREEN, BLUE], size=3, spacing=2)
    if idx == 20:
        from adafruit_led_animation.animation.pacman import PacMan
        return PacMan(pixels, speed=0.05, color=YELLOW, tail_length=3, bounce=True)
    if idx == 21:
        from adafruit_led_animation.animation.blink import Blink
        return Blink(pixels, speed=0.5, color=PINK, background_color=TEAL)


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
            else:
                print(f"No state {idx}")
        except ValueError:
            print("Enter an integer")
    current.animate()