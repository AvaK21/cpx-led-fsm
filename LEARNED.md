# LEARNED.md

Lessons from running `adafruit_led_animation` on an ATSAMD21G18 (Circuit Playground Express, 32KB RAM).

These are real failure modes hit during development, not theoretical warnings.

---

## 1. The SAMD21 Memory Budget Is Brutal

**Total RAM: 32KB.** After CircuitPython core boots and `neopixel` + `adafruit_led_animation` are imported, available heap is approximately **5,500–6,000 bytes**. That is your entire working budget for animation objects, local variables, and anything else your program needs at runtime.

For context: a single `Rainbow` animation precomputes a 256-step color table requiring **1,024 contiguous bytes**. One animation can consume ~17% of your remaining heap.

---

## 2. `gc.collect()` Cannot Free Imported Modules

**Symptom:** `gc.collect()` was called before each animation instantiation. Memory still declined monotonically across state transitions.

**Why:** `gc.collect()` reclaims *objects* with zero references. It cannot unload a module. Once a module is imported into `sys.modules`, its bytecode, class definitions, and constants are permanently resident for the life of the program.

**What was tried:**
```python
for mod_name in list(sys.modules):
    if mod_name.startswith("adafruit_led_animation.animation"):
        del sys.modules[mod_name]
gc.collect()
```
**Result:** No measurable memory recovery.

**Why that also failed:** The real culprit is the **qstr pool** — CircuitPython interns every identifier (variable names, attribute names, class names) encountered into a global string table. This pool is never garbage collected by design. Each new animation class imported permanently adds its identifiers to the qstr pool for the life of the session, regardless of `del sys.modules[...]`.

**Measured evidence:**
```
State 0 | free: 5872
State 1 | free: 4208
State 3 | free: 1584
State 4 → MemoryError: allocating 160 bytes
```

Each unique animation class imported cost ~800–1,600 bytes permanently. By state 4, even a 160-byte allocation failed.

---

## 3. Lazy Imports Delay the Cost, They Don't Eliminate It

**Initial fix (partial):** Move imports inside `make_state()` so only the active animation's module is imported at instantiation time.

**Result:** Deferred the crash — didn't prevent it. The first time each animation class is reached, its module gets imported and the qstr cost is permanently paid. Revisiting a previously loaded state doesn't re-pay qstr cost, but accumulated imports across a session still exhaust the pool.

**Lesson:** On SAMD21, treat each unique `import` as a permanent, non-recoverable RAM expenditure. There is no mechanism to reclaim it short of a hard reset.

---

## 4. The Correct Testing Workflow: Exploit the Auto-Reload Reset

**The constraint:** After 1–3 unique state transitions, the SAMD21 heap is typically exhausted. You cannot test all animations in a single session.

**The workflow:**

1. Change the start state at the bottom of the batch file:
   ```python
   current = make_state(2)  # start on the state you want to test
   ```
2. Save the file — CircuitPython auto-reloads on file save, triggering a **hard reset**
3. Hard reset clears the qstr pool, heap, and all module state entirely
4. You get a clean ~5,800 bytes free for the new session

This is not a workaround. It is the correct approach for this class of hardware. The auto-reload mechanism is effectively a free "restart with different boot state" — use it deliberately rather than fighting memory mid-session.

---

## 5. `MemoryError` on Contiguous Allocation ≠ "Out of Memory"

The error `MemoryError: memory allocation failed, allocating 1024 bytes` can occur even when total free memory exceeds 1,024 bytes. The SAMD21 does not have virtual memory. If the heap is fragmented — many small allocations interspersed with freed gaps — a large *contiguous* block may not exist even though the sum of free gaps is sufficient.

`Rainbow` is particularly vulnerable because it precomputes its full color table as one contiguous allocation. Fix: use `step=4` to reduce table size from 256 to 64 entries.

```python
Rainbow(pixels, speed=0.05, period=2, step=4)  # not step=1 (default)
```

---

## 6. Two NeoPixel Owners = Immediate Crash

**Symptom:** `ValueError: NEOPIXEL in use` at `neopixel.NeoPixel(board.NEOPIXEL, ...)`.

**Cause:** Importing `adafruit_circuitplayground.cp` silently instantiates `cp.pixels` — a `NeoPixel` object bound to `board.NEOPIXEL`. CircuitPython locks hardware pins on assignment. A second `neopixel.NeoPixel(board.NEOPIXEL, ...)` call collides with the already-claimed pin.

**Fix:** Pick one abstraction level. Either use `cp.pixels` throughout, or don't import `cp` at all and use raw `neopixel.NeoPixel`. Never mix both.

```python
# Wrong — two owners of NEOPIXEL
from adafruit_circuitplayground import cp
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, ...)  # crashes

# Right — one owner
from adafruit_circuitplayground import cp
pixels = cp.pixels
pixels.brightness = 0.05
pixels.auto_write = False
```

---

## 7. Instrumentation Worth Keeping

Add this line on successful state transitions during development:

```python
if new_state:
    current = new_state
    print(f"State {idx} | free: {gc.mem_free()}")
else:
    print(f"No state {idx}")
```

Note the placement: print on success (inside `if new_state`), not on failure. A declining `mem_free()` across transitions confirms qstr accumulation — your crash warning is approaching ~1,000 bytes free.

---

## 8. CustomColorChase Exists (Contrary to Earlier Assumptions)

`adafruit_led_animation.animation.customcolorchase.CustomColorChase` is a real class in the bundle — confirmed working. Earlier documentation in this repo incorrectly stated it didn't exist. Always verify against the actual bundle contents rather than documentation:

```python
import os
print(os.listdir('/lib/adafruit_led_animation/animation/'))
```

---

## Summary

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| `MemoryError` on `Rainbow` init | 1024-byte contiguous alloc fails on fragmented heap | `step=4` reduces table size |
| Memory depletes across state transitions | qstr pool grows permanently per unique import | Batch files + reload between sessions |
| `gc.collect()` + `del sys.modules` doesn't recover memory | qstr pool is never GC'd by design | Accept it; exploit auto-reload reset |
| `ValueError: NEOPIXEL in use` | Two owners of same hardware pin | Use `cp.pixels` or raw `neopixel`, never both |
| Lazy imports didn't fully solve the problem | Same qstr accumulation, just deferred | Batching + intentional start state solves what lazy imports can't |
