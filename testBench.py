import asyncio
from bleak import BleakScanner, BleakClient
import logging
import struct
logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.INFO)
address = "d0:3e:7d:0f:48:52"
UUID = "0000181b-0000-1000-8000-00805f9b34fb"
#https://github.com/wiecosystem/Bluetooth/blob/master/doc/devices/huami.health.scale2.md
#they have code on that repo with bluetooth already working, for some reason there is a if looking for 22. I think if you find the right call you can just get the full byte array


# async def main():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d.details)sudo rebo


# async def main():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d.details)
#         if d.name == 'MIBFS':
#             print('Found it')
#
#
#     async with BleakClient(address) as client:
#         svcs = await client.get_services()
#         print("Services:")
#         for service in svcs:
#             print(service)
#             data = await client.read_gatt_descriptor(service)
#             print(data)
#
#
#
#         print(data)
# async def services():
#
#     device = await BleakScanner.find_device_by_address(address)
#     async with BleakClient(device) as client:
#         #await client.connect()
#         # await client.pair(3)
#         #await client.write_gatt_char('00001542-0000-3512-2118-0009af100700', b'\x06\x04\x00\x01')
#
#         for service in client.services:
#             for char in service.characteristics:
#                 if "read" in char.properties:
#                     try:
#                         value = await client.read_gatt_char(char.uuid)
#
#                         logger.info(
#                             "  [Characteristic] %s (%s), Value: %r",
#                             char,
#                             ",".join(char.properties),
#                             value,
#                         )
#                     except Exception as e:
#                         logger.error(
#                             "  [Characteristic] %s (%s), Error: %s",
#                             char,
#                             ",".join(char.properties),
#                             e,
#                         )
#
#                 else:
#                     logger.info(
#                         "  [Characteristic] %s (%s)", char, ",".join(char.properties)
#                     )
#
#                 for descriptor in char.descriptors:
#                     try:
#                         value = await client.read_gatt_char(char.uuid)
#                         logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
#                     except Exception as e:
#                         logger.error("    [Descriptor] %s, Error: %s", descriptor, e)
#
#         # await client.unpair()
#
#
# asyncio.run(services())

# import sys
# import datetime
# import random
# from struct import *
# from bluepy import btle
#
#
#
# class miScale(btle.DefaultDelegate):
#     def __init__(self):
#         btle.DefaultDelegate.__init__(self)
#
#         self.address = address
#         self.height = 175
#         self.age = 26
#         self.sex = 1
#
#     def handleDiscovery(self, dev, isNewDev, isNewData):
#         if dev.addr == self.address:
#             for (adType, desc, value) in dev.getScanData():
#                 if adType == 22:
#                     data = bytes.fromhex(value[4:])
#                     ctrlByte0 = data[0]
#                     ctrlByte1 = data[1]
#
#                     emptyLoad = ctrlByte1 & (1<<7)
#                     isStabilized = ctrlByte1 & (1<<5)
#                     hasImpedance = ctrlByte1 & (1<<1)
#
#
#                     if emptyLoad:
#                         print("(no load)")
#
#                     print("New packet")
#                     if isStabilized:
#                         print("New stabilized weight")
#                     if hasImpedance:
#                         print("New impedance")
#
#                     print("\t Control bytes = {0:08b}/{1:08b}".format(ctrlByte0, ctrlByte1))
#                     print("\t Date = {}/{}/{} {}:{}:{}".format(int(data[5]), int(data[4]), int((data[3] << 8) | data[2]), int(data[6]), int(data[7]), int(data[8])))
#
#                     impedance = ((data[10] & 0xFF) << 8) | (data[9] & 0xFF)
#                     weight = (((data[12] & 0xFF) << 8) | (data[11] & 0xFF)) / 200.0
#
#                     print("\t impedance is {}".format(impedance))
#                     print("\t weight is {}".format(weight))
#
#
#
#                 elif adType == 1 or adType ==  2 or adType == 9:
#                     continue
#                 elif adType == 255:
#                     continue
#                 else:
#                     print("=> new unknown packet: type={} data={}".format(adType, value))
#
#     def run(self):
#         scanner = btle.Scanner()
#         scanner.withDelegate(self)
#         while True:
#             scanner.start()
#             scanner.process(1)
#             scanner.stop()
#
# scale = miScale()
# scale.run()

import asyncio
from uuid import UUID

from construct import Array, Byte, Const, Int8sl, Int16ub, Struct
from construct.core import ConstError

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


def device_found(
    device: BLEDevice, advertisement_data: AdvertisementData
):
    """Decode iBeacon."""
    if device.address != address.upper():
        return
    try:
        scale_package = advertisement_data.service_data['0000181b-0000-1000-8000-00805f9b34fb']
        impedance = ((scale_package[10] & 0xFF) << 8) | (scale_package[9] & 0xFF)
        weight = (((scale_package[12] & 0xFF) << 8) | (scale_package[11] & 0xFF))/100.0

        print(impedance)
        print(weight)
    except KeyError:
        # Apple company ID (0x004c) not found
        pass
    except ConstError:
        # No iBeacon (type 0x02 and length 0x15)
        pass


async def main():
    """Scan for devices."""
    scanner = BleakScanner()
    scanner.register_detection_callback(device_found)

    while True:
        await scanner.start()
        await asyncio.sleep(1.0)
        await scanner.stop()


asyncio.run(main())