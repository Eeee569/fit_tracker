import asyncio, threading
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from settings import Settings
import time

class ScaleReader:
    """Read data from Xiaomi Mi Scale 2."""

    def __init__(self):
        self.data_tuple = (0, 0)
        self.scanner = BleakScanner()
        self.scanner.register_detection_callback(self.device_found)

    def device_found(self,
        device: BLEDevice, advertisement_data: AdvertisementData
    ):
        """Decode huamisclae2 package."""
        if device.address != Settings.scale_address:
            return
        try:
            scale_package = advertisement_data.service_data[Settings.metrics_uuid]
            impedance = ((scale_package[10] & 0xFF) << 8) | (scale_package[9] & 0xFF)
            weight = (((scale_package[12] & 0xFF) << 8) | (scale_package[11] & 0xFF))/100.0

            self.data_tuple = (impedance, weight)
        except :
            self.data_tuple = (0, 0)
            pass

    async def run(self):
        await self.scanner.start()
        await asyncio.sleep(1.0)
        await self.scanner.stop()
        return self.data_tuple
async def test_func():
    """Scan for devices."""
    print("test")
    reader = ScaleReader()
    scanner = BleakScanner()
    scanner.register_detection_callback(reader.device_found)
    start = time.time()
    while True:
        await scanner.start()
        await asyncio.sleep(1.0)
        await scanner.stop()

        print(reader.data_tuple)
        if reader.data_tuple == (0, 0):
            print(f"*******************************************************{time.time()-start}")



_loop = None

if __name__ == "__main__":
    asyncio.run(test_func())

# def fire_and_forget(coro):
#     global _loop
#     if _loop is None:
#         _loop = asyncio.new_event_loop()
#         threading.Thread(target=_loop.run_forever, daemon=True).start()
#     _loop.call_soon_threadsafe(asyncio.create_task, coro)


# if __name__ == "__main__":
#
#     fire_and_forget(test_func())
#
#     print("Done")
#     time.sleep(100)