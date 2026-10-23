import board
import digitalio
import storage

# Hold Shift (GP7 -> GND) while plugging in USB to show CIRCUITPY drive
shift_key = digitalio.DigitalInOut(board.GP7)
shift_key.direction = digitalio.Direction.INPUT
shift_key.pull = digitalio.Pull.UP

if shift_key.value:
    storage.disable_usb_drive()

shift_key.deinit()