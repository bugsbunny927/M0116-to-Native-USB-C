Apple Standard Keyboard (M0116) USB-C ConversionA clean, non-destructive USB-C conversion for the Apple M0116 keyboard using a Waveshare RP2040-Zero and pure CircuitPython.Instead of desoldering all 81 Alps switches or buying an aftermarket PCB, this mod bypasses a dead stock controller (NEC 8048 clone) by soldering directly to the 40-pin DIP socket pins on the solder side of the board.HighlightsNo switch desoldering: Keeps the original PCB and Alps switches completely intact.Pure CircuitPython: No QMK compilation required. Runs directly off code.py.Hardware matrix mapping: Taps rows, columns, and modifier pins straight from the 40-pin chip socket.Latching Caps Lock support: Alps mechanical lock toggle switch is handled with press/release tap logic on every state transition.Silent boot with failsafe: boot.py hides the CIRCUITPY drive on startup. Hold Shift while plugging in to show the drive for editing.Wiring Pinout (Socket to RP2040-Zero)All signals are taken from the rear through-hole pads of the 40-pin MCU socket:CategoryDIP Socket PinRP2040-Zero PinGroundPin 20 (VSS)GNDMatrix Rows (0–9)Pins 34, 33, 32, 31, 30, 29, 28, 27, 22, 21GP0–GP5, GP26–GP29Matrix Cols (0–7)Pins 12, 13, 14, 15, 16, 17, 18, 19GP8–GP15ModifiersControl (36), Shift (37)GP6, GP7Underside PadsOption (23), Command (24), Caps Lock (6), Power (35)GP17, GP18, GP19, GP20⚠️ Warning: Do not connect to Socket Pins 26 or 40 (original +5V rails).Software SetupFlash standard CircuitPython 9.x/10.x onto the RP2040-Zero.Copy code.py to the root of the CIRCUITPY drive.Add boot.py to silence the USB flash drive window on connect:import board, digitalio, storage

shift = digitalio.DigitalInOut(board.GP7)
shift.direction = digitalio.Direction.INPUT
shift.pull = digitalio.Pull.UP

# Suppress CIRCUITPY unless Shift is held on plug-in
if shift.value:
    storage.disable_usb_drive()

shift.deinit()
UsageDaily use: Plug in and type immediately. No drive letters or File Explorer pop-ups.Firmware updates: Hold Shift while plugging into USB to expose the CIRCUITPY filesystem.LicenseMIT
