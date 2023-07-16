import asyncio
import time
from bleak import BleakClient,BleakScanner

peripheral_address = "REPLACE_THIS_WITH_YOUR_TIMEFLIP_DEVICE_ADDRESS".lower()
battery_level_uuid_str = "00002A19-0000-1000-8000-00805F9B34FB".lower()
password_uuid_str = "F1196F57-71A4-11E6-BDF4-0800200C9A66".lower()
facet_uuid_str = "F1196F52-71A4-11E6-BDF4-0800200C9A66".lower()

def print_facet(data):
    print(f"Facets: {int.from_bytes(data, byteorder='little')}")

def callback(sender, data):
    print_facet(data)

async def main():
   async with BleakClient(peripheral_address, loop=loop) as device:
       device.connect()

       battery_level = await device.read_gatt_char(battery_level_uuid_str)
       print(f"Battery Level: {battery_level[0]}")

       password_value = bytearray(b"\x30\x30\x30\x30\x30\x30")  # "000000" as bytes
       await device.write_gatt_char(password_uuid_str, password_value, response=True)
       print("Password characteristic written")

       facet_read = await device.read_gatt_char(facet_uuid_str)
       print_facet(facet_read)

       await device.start_notify(facet_uuid_str, callback)
       await asyncio.sleep(30)
       await device.disconnect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())