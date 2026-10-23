# Apple M0116 keyboard, controller chip replaced by an RP2040-Zero  ->  USB HID keyboard
# CircuitPython 9.x / 10.x.  No extra libraries needed.
#
# HOW IT WORKS
#   1. With KEYS empty (below) this file runs LEARN MODE: you press every key once and it works
#      out which two wired GPIO pins each key connects. It prints a KEYS table.
#   2. Paste that table over the empty KEYS = {} below, save, and the board becomes a USB keyboard.
#
# Learn mode needs no knowledge of the wiring: every GPIO that exists on the board is tested, and
# the ones with nothing connected simply never show up.

import time
import board
import digitalio
import supervisor
import sys
import usb_hid

# ----- paste the table printed by learn mode here ----------------------------------------------
# control, the two shifts, caps_lock, option and command each ground one sense pin when pressed
# (pins 6, 7, 19, 17, 18), so one pair each is enough to detect them.
KEYS = {
    "d": ((13, 27), (27, 13)),
    "f": ((12, 27), (27, 12)),
    "a": ((15, 27), (27, 15)),
    "g": ((11, 27), (27, 11)),
    "c": ((13, 26), (26, 13)),
    "b": ((11, 26), (26, 11)),
    "m": ((9, 26), (26, 9)),
    "comma": ((8, 26), (26, 8)),
    "l": ((0, 12), (12, 0)),
    "n": ((10, 26), (26, 10)),
    "o": ((1, 9), (9, 1)),
    "i": ((1, 8), (8, 1)),
    "h": ((10, 27), (27, 10)),
    "j": ((9, 27), (27, 9)),
    "u": ((8, 29), (29, 8)),
    "esc": ((3, 15), (15, 3)),
    "t": ((10, 29), (29, 10)),
    "v": ((12, 26), (26, 12)),
    "w": ((13, 29), (29, 13)),
    "k": ((8, 27), (27, 8)),
    "s": ((14, 27), (27, 14)),
    "r": ((11, 29), (29, 11)),
    "semicolon": ((1, 14), (14, 1)),
    "rshift": ((0, 7),),
    "equals": ((0, 10), (10, 0)),
    "q": ((14, 29), (29, 14)),
    "y": ((9, 29), (29, 9)),
    "x": ((14, 26), (26, 14)),
    "left": ((5, 14), (14, 5)),
    "z": ((15, 26), (26, 15)),
    "clear": ((4, 12), (12, 4)),
    "rbracket": ((1, 12), (12, 1)),
    "p": ((1, 10), (10, 1)),
    "space": ((5, 15), (15, 5)),
    "kp_enter": ((4, 11), (11, 4)),
    "right": ((5, 8), (8, 5)),
    "kp_period": ((5, 11), (11, 5)),
    "kp8": ((2, 13), (13, 2)),
    "kp9": ((2, 14), (14, 2)),
    "kp6": ((2, 10), (10, 2)),
    "kp7": ((2, 12), (12, 2)),
    "backslash": ((5, 13), (13, 5)),
    "kp4": ((2, 8), (8, 2)),
    "kp5": ((2, 9), (9, 2)),
    "kp_minus": ((2, 15), (15, 2)),
    "kp2": ((4, 9), (9, 4)),
    "kp1": ((4, 8), (8, 4)),
    "return": ((1, 13), (13, 1)),
    "4": ((3, 11), (11, 3)),
    "7": ((9, 28), (28, 9)),
    "6": ((3, 9), (9, 3)),
    "1": ((3, 14), (14, 3)),
    "0": ((0, 8), (8, 0)),
    "3": ((3, 12), (12, 3)),
    "2": ((3, 13), (13, 3)),
    "tab": ((15, 29), (29, 15)),
    "down": ((5, 10), (10, 5)),
    "5": ((3, 10), (10, 3)),
    "kp_plus": ((2, 11), (11, 2)),
    "9": ((3, 8), (8, 3)),
    "8": ((8, 28), (28, 8)),
    "delete": ((0, 11), (11, 0)),
    "kp3": ((4, 10), (10, 4)),
    "period": ((0, 13), (13, 0)),
    "slash": ((0, 14), (14, 0)),
    "up": ((0, 15), (15, 0)),
    "kp_asterisk": ((4, 15), (15, 4)),
    "control": ((0, 6),),
    "kp_slash": ((4, 14), (14, 4)),
    "grave": ((5, 12), (12, 5)),
    "kp0": ((5, 9), (9, 5)),
    "minus": ((0, 9), (9, 0)),
    "lshift": ((0, 7),),
    "kp_equals": ((4, 13), (13, 4)),
    "quote": ((1, 15), (15, 1)),
    "e": ((12, 29), (29, 12)),
    "lbracket": ((1, 11), (11, 1)),
    "caps_lock": ((0, 19),),
    "option": ((0, 17),),
    "command": ((0, 18),),
}
# -----------------------------------------------------------------------------------------------

# Candidate GPIOs: every GPIO the board defines (the extra pads on the back included).
# Ones that do not exist on the board are skipped automatically.
CANDIDATES = list(range(0, 30))

# To learn only some keys (keeps everything already in KEYS), list them here, e.g.
# LEARN_ONLY = ["caps_lock", "option", "command"]. Leave as None for normal use.
LEARN_ONLY = None

# Learn-mode prompts, in physical order, with the USB HID usage each key becomes.
# Modifiers are given as ("mod", bit).
LAYOUT = [
    ("esc", 0x29), ("1", 0x1E), ("2", 0x1F), ("3", 0x20), ("4", 0x21), ("5", 0x22),
    ("6", 0x23), ("7", 0x24), ("8", 0x25), ("9", 0x26), ("0", 0x27), ("minus", 0x2D),
    ("equals", 0x2E), ("delete", 0x2A),
    ("tab", 0x2B), ("q", 0x14), ("w", 0x1A), ("e", 0x08), ("r", 0x15), ("t", 0x17),
    ("y", 0x1C), ("u", 0x18), ("i", 0x0C), ("o", 0x12), ("p", 0x13),
    ("lbracket", 0x2F), ("rbracket", 0x30),
    ("control", ("mod", 0x01)), ("a", 0x04), ("s", 0x16), ("d", 0x07), ("f", 0x09),
    ("g", 0x0A), ("h", 0x0B), ("j", 0x0D), ("k", 0x0E), ("l", 0x0F),
    ("semicolon", 0x33), ("quote", 0x34), ("return", 0x28),
    ("lshift", ("mod", 0x02)), ("z", 0x1D), ("x", 0x1B), ("c", 0x06), ("v", 0x19),
    ("b", 0x05), ("n", 0x11), ("m", 0x10), ("comma", 0x36), ("period", 0x37),
    ("slash", 0x38), ("rshift", ("mod", 0x20)),
    ("caps_lock", 0x39), ("option", ("mod", 0x04)), ("command", ("mod", 0x08)),
    ("grave", 0x35), ("space", 0x2C), ("backslash", 0x31),
    ("left", 0x50), ("right", 0x4F), ("down", 0x51), ("up", 0x52),
    # keypad
    ("clear", 0x53), ("kp_equals", 0x67), ("kp_slash", 0x54), ("kp_asterisk", 0x55),
    ("kp7", 0x5F), ("kp8", 0x60), ("kp9", 0x61), ("kp_plus", 0x57),
    ("kp4", 0x5C), ("kp5", 0x5D), ("kp6", 0x5E), ("kp_minus", 0x56),
    ("kp1", 0x59), ("kp2", 0x5A), ("kp3", 0x5B), ("kp_enter", 0x58),
    ("kp0", 0x62), ("kp_period", 0x63),
]
USAGE = dict(LAYOUT)

# ----- GPIO setup and scanning ------------------------------------------------------------------
pins = {}
for n in CANDIDATES:
    try:
        p = digitalio.DigitalInOut(getattr(board, "GP%d" % n))
    except (AttributeError, ValueError):
        continue
    p.switch_to_input(pull=digitalio.Pull.UP)
    pins[n] = p


def scan_pairs(drivers=None):
    """Return {(a, b)}: driving pin a low pulls pin b low, i.e. a closed key between a and b."""
    found = set()
    for a in (drivers if drivers is not None else list(pins)):
        pa = pins[a]
        pa.switch_to_output(value=False)
        for b, pb in pins.items():
            if b != a and not pb.value:
                found.add((a, b))
        pa.switch_to_input(pull=digitalio.Pull.UP)
    return found


def stable_scan(drivers=None, count=3):
    """Scan until `count` consecutive scans agree (simple debounce)."""
    last = scan_pairs(drivers)
    same = 1
    tries = 0
    while same < count and tries < 200:
        tries += 1
        cur = scan_pairs(drivers)
        if cur == last:
            same += 1
        else:
            last, same = cur, 1
    return last


# ----- LEARN MODE -------------------------------------------------------------------------------
def learn():
    print()
    print("=== LEARN MODE ===")
    print("GPIOs found on this board:", sorted(pins))
    print("Release every key (caps lock UP). Starting in 8 seconds...")
    for i in range(8, 0, -1):
        print(i)
        time.sleep(1)
    print("Measuring idle state...")
    baseline = stable_scan() | stable_scan()
    print("Idle state measured.")
    if baseline:
        print("Note: these pin pairs are always connected and will be ignored:", sorted(baseline))
    learned = {}
    used = {}
    todo = [n for n, _ in LAYOUT if LEARN_ONLY is None or n in LEARN_ONLY]
    for name in todo:
        extra = "  (press it DOWN; it stays down)" if name == "caps_lock" else ""
        print("Press and HOLD:", name, extra, "   [type s then Enter to skip]")
        while True:
            if supervisor.runtime.serial_bytes_available:
                if sys.stdin.read(1).lower() == "s":
                    print("  skipped", name)
                    break
            new = scan_pairs() - baseline
            if not new:
                continue
            new = stable_scan() - baseline
            if not new:
                continue
            pairs = tuple(sorted(new))
            if pairs in used:
                print("  WARNING: same pins as", used[pairs], "- wiring or order problem?")
            used[pairs] = name
            learned[name] = pairs
            print("  got", name, pairs)
            break
        extra2 = " (press caps lock again to release it)" if name == "caps_lock" else ""
        print("  release it" + extra2)
        while scan_pairs() - baseline:
            time.sleep(0.05)
        time.sleep(0.15)
    print()
    print("=== DONE. Copy the lines between the dashes. ===")
    if LEARN_ONLY is None:
        print("Paste them over  KEYS = {}  at the top.")
    else:
        print("Paste these lines INSIDE the existing KEYS = { ... } table, then set LEARN_ONLY = None.")
    print("-----")
    if LEARN_ONLY is None:
        print("KEYS = {")
    for name, pairs in learned.items():
        print('    "%s": %r,' % (name, pairs))
    if LEARN_ONLY is None:
        print("}")
    print("-----")
    missing = [n for n in todo if n not in learned]
    if missing:
        print("Not learned:", missing)
    while True:
        time.sleep(1)


# ----- NORMAL MODE: USB keyboard ----------------------------------------------------------------
def run():
    kbd = None
    for d in usb_hid.devices:
        if d.usage_page == 0x01 and d.usage == 0x06:
            kbd = d
            break
    if kbd is None:
        raise RuntimeError("No USB keyboard HID device")

    drivers = sorted({a for pairs in KEYS.values() for (a, _) in pairs})
    held = []
    mods = 0

    def send():
        keys = held[:6]
        kbd.send_report(bytes([mods, 0] + keys + [0] * (6 - len(keys))))

    down = set()
    while True:
        seen = stable_scan(drivers, 2)
        now_down = {name for name, pairs in KEYS.items() if all(p in seen for p in pairs)}
        if now_down != down:
            for name in now_down ^ down:
                usage = USAGE.get(name)
                if usage is None:
                    continue
                pressed = name in now_down
                if name == "caps_lock":          # latching key: every change = one tap
                    held.append(0x39)
                    send()
                    held.remove(0x39)
                    send()
                elif isinstance(usage, tuple):
                    if pressed:
                        mods |= usage[1]
                    else:
                        mods &= ~usage[1]
                    send()
                else:
                    if pressed and usage not in held:
                        held.append(usage)
                    elif not pressed and usage in held:
                        held.remove(usage)
                    send()
            down = now_down
        time.sleep(0.002)


if KEYS and LEARN_ONLY is None:
    run()
else:
    learn()
