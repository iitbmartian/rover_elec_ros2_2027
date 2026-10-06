import time
import odrive
from odrive.enums import AxisState
from odrive.utils import request_state, dump_errors

odrv_1 = odrive.find_sync(
    serial_number=["261832805677"],
    interfaces=["can:can0"],
)

print("Odrive ID: ", odrv_1.serial_number)

for i in range(5):
    odrv_1.set_gpio(9,False)
    time.sleep(0.5)

    odrv_1.sey_gpio(9,True)
    time.sleep(0.5)
