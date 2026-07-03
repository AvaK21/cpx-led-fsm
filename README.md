# cpx-led-fsm

A test project for exploring `adafruit_led_animation` animations on the **Adafruit Circuit Playground Express (CPX)** using a simple integer-driven state selector over the serial console.

Not a production state machine. Exists to answer: *what does this animation actually look like on 10 NeoPixels?*

---

## Hardware

| Component | Detail |
|-----------|--------|
| Board | Adafruit Circuit Playground Express |
| MCU | ATSAMD21G18 (32KB RAM) |
| Pixels | 10x onboard NeoPixels (`board.NEOPIXEL`) |
| Firmware | CircuitPython 10.2.1 |

---

## Dependencies

From the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries):

```
lib/
  adafruit_led_animation/
  neopixel.mpy
```

Install via `circup`:
```bash
circup install adafruit_led_animation neopixel
```

Or copy `adafruit_led_animation/` folder manually from the bundle into `CIRCUITPY/lib/`.

---

## Usage

1. Copy a batch file to `CIRCUITPY/code.py` — auto-reload triggers on save
2. Open a serial console (Mu, Thonny, or `screen /dev/ttyACM0 115200`)
3. Type an integer and press Enter to switch animation state

```
> 1
State 1 | free: 4208
```

**Testing workflow for memory-constrained sessions:** After 1–3 unique state transitions, the SAMD21 heap is typically exhausted. To test a specific animation:

1. Change the start state at the bottom of the file: `current = make_state(X)`
2. Save — CircuitPython auto-reloads, hard-resetting the qstr pool and heap
3. You get a clean slate for each reload

This is not a workaround. It is the correct approach for this hardware. See [LEARNED.md](./LEARNED.md).

---

## Batch Files

Due to SAMD21 memory constraints, animations are split across batch files.  
Copy the desired batch to `code.py` to test it.

### `basic.py`

General-purpose animations. Good starting point.

| State | Class | Notes |
|-------|-------|-------|
| 0 | `Pulse` | Blue breathe |
| 1 | `Comet` | Green — good loading indicator candidate |
| 2 | `Blink` | Red on/off |
| 3 | `Chase` | Green — arcade marquee look |
| 4 | `Solid` | Static teal fill |
| 5 | `Blink` | Pink + teal `background_color` — alternates between two colors |

### `rainbow.py`

All rainbow variants.

| State | Class | Notes |
|-------|-------|-------|
| 0 | `Rainbow` | Full color wheel cycle |
| 1 | `RainbowChase` | Marquee with rainbow colors |
| 2 | `RainbowSparkle` | Random rainbow pixel flashes |
| 3 | `RainbowComet` | Bouncing rainbow comet — standout on 10 pixels |

### `random.py`

Cycle and sparkle variants.

| State | Class | Notes |
|-------|-------|-------|
| 0 | `ColorCycle` | All pixels cycle through colors together |
| 1 | `Sparkle` | A few random pixels flash purple at a time |
| 2 | `SparklePulse` | Random pixels fade in and out — sparkle with easing |

### `custom_color.py`

Multi-color chase variants. Partially tested.

| State | Class | Notes |
|-------|-------|-------|
| 0 | `CustomColorChase` | Yellow/Purple/Orange chase — confirmed working |
| — | More TBD | Only state 0 tested |

---

## Confirmed Animation Inventory

All animations verified to exist in the installed bundle:

| Module | Class |
|--------|-------|
| `animation.blink` | `Blink` |
| `animation.solid` | `Solid` |
| `animation.colorcycle` | `ColorCycle` |
| `animation.chase` | `Chase` |
| `animation.comet` | `Comet` |
| `animation.pulse` | `Pulse` |
| `animation.rainbow` | `Rainbow` |
| `animation.sparkle` | `Sparkle` |
| `animation.rainbowchase` | `RainbowChase` |
| `animation.rainbowcomet` | `RainbowComet` |
| `animation.rainbowsparkle` | `RainbowSparkle` |
| `animation.sparklepulse` | `SparklePulse` |
| `animation.customcolorchase` | `CustomColorChase` |

> Verify what's in your specific bundle:
> ```python
> import os; print(os.listdir('/lib/adafruit_led_animation/animation/'))
> ```

---

## Memory Notes

The SAMD21 has 32KB RAM. After boot and imports, approximately **5,500–6,000 bytes** remain.
Each unique animation class imported costs ~800–1,600 bytes **permanently** per session — not recoverable via `gc.collect()`.

Full breakdown → [LEARNED.md](./LEARNED.md)
