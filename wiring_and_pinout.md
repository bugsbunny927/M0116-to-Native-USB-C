# Apple Standard Keyboard (M0116) RP2040-Zero Pinout & Wiring Guide

This document details the complete 25-wire pinout mapping between the Apple M0116's original 40-pin DIP controller socket (solder-side pin tips) and the Waveshare RP2040-Zero microcontroller.

---

## 1. Socket Orientation & Pin Numbering

The 40-pin DIP socket on the PCB follows standard dual in-line package numbering:
* **Pin 1:** Bottom-left (notch facing left/up depending on orientation).
* **Pins 1 to 20:** Run left-to-right along the bottom row.
* **Pins 21 to 40:** Counter-clockwise return along the top row (Pin 21 opposite Pin 20; Pin 40 opposite Pin 1).

---

## 2. Master Wiring & Color Code Table

Total connections: **25 wires** (10 Rows + 8 Columns + 6 Direct Modifiers + 1 Common Ground).

| Signal Group | Signal Name / Function | DIP Socket Pin | RP2040-Zero Pin | Wire Color | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ground** | System Ground (`VSS`) | **Pin 20** | **GND** | **Black** | Common logic reference |
| **Matrix Rows** | Row 0 (Up Arrow) | **Pin 34** | **GP0** | **Yellow** | Outer edge pad |
| | Row 1 (Quote `'`) | **Pin 33** | **GP1** | **Yellow** | Outer edge pad |
| | Row 2 (Numpad `-`) | **Pin 32** | **GP2** | **Yellow** | Outer edge pad |
| | Row 3 (Esc) | **Pin 31** | **GP3** | **Yellow** | Outer edge pad |
| | Row 4 (Numpad `*`) | **Pin 30** | **GP4** | **Yellow** | Outer edge pad |
| | Row 5 (Spacebar) | **Pin 29** | **GP5** | **Yellow** | Outer edge pad |
| | Row 6 (`Z`) | **Pin 28** | **GP26** | **Yellow** | Outer edge pad |
| | Row 7 (`A`) | **Pin 27** | **GP27** | **Yellow** | Outer edge pad |
| | Row 8 (Digit `8`) | **Pin 22** | **GP28** | **Yellow** | Outer edge pad |
| | Row 9 (Tab) | **Pin 21** | **GP29** | **Yellow** | Outer edge pad |
| **Matrix Cols** | Column 0 | **Pin 12** | **GP8** | **Green** | Outer edge pad |
| | Column 1 | **Pin 13** | **GP9** | **Green** | Outer edge pad |
| | Column 2 | **Pin 14** | **GP10** | **Green** | Outer edge pad |
| | Column 3 | **Pin 15** | **GP11** | **Green** | Outer edge pad |
| | Column 4 | **Pin 16** | **GP12** | **Green** | Outer edge pad |
| | Column 5 | **Pin 17** | **GP13** | **Green** | Outer edge pad |
| | Column 6 | **Pin 18** | **GP14** | **Green** | Outer edge pad |
| | Column 7 | **Pin 19** | **GP15** | **Green** | Outer edge pad |
| **Modifiers** | Control | **Pin 36** | **GP6** | **Blue** | Direct-to-ground switch |
| | Shift (L/R Shift tied) | **Pin 37** | **GP7** | **Blue** | Direct-to-ground switch |
| | Option / Alt | **Pin 23** | **GP17** | **Blue** | Underside flat pad 1 |
| | Command / GUI | **Pin 24** | **GP18** | **Blue** | Underside flat pad 2 |
| **Special Keys** | Locking Caps Lock | **Pin 6** | **GP19** | **White** | Underside flat pad 3 (Mechanical latch) |
| | Top Power Key ($\triangle$) | **Pin 35** | **GP20** | **White** | Underside flat pad 4 |

---

## 3. Unconnected / Ignored Socket Pins

Do **not** solder to the following pins on the 40-pin DIP footprint:

* **Pins 1, 7:** Original controller ground references (`T0`, `EA` tied to GND on PCB).
* **Pins 26, 40:** Old $+5\text{V}$ power rails from the original host ADB supply. **Leave completely disconnected.**
* **Pins 2–5, 8–11, 25, 38, 39:** Unused/open traces on the OEM PCB.
* **RP2040 5V / 3V3 Pins:** Left unconnected (powered directly via onboard USB-C connection).

---

## 4. Hardware Construction Notes

1. **Underside Solder Pads (RP2040-Zero):**
   * Pre-tin `GP17`, `GP18`, `GP19`, and `GP20` prior to placement.
   * Apply Kapton tape or electrical tape beneath the RP2040-Zero to prevent shorting against PCB traces.
2. **Solder Points:** Solder thin 30 AWG kynar/wrapping wire directly to the exposed solder tails of the 40-pin DIP socket on the rear of the keyboard PCB.
3. **Strain Relief:** Secure the wire bundles with electrical or cloth harness tape before closing the chassis.