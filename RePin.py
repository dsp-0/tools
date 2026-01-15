import asyncio
import sys
from bleak import BleakClient, BleakScanner

async def find_and_write_to_device(service_uuid, char_uuid, value):
    # Поиск устройства по UUID сервиса
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: service_uuid.lower() in ad.service_uuids
    )

    if device is None:
        print(f"Устройство с сервисом UUID {service_uuid} не найдено.")
        return

    print(f"Найдено устройство: {device.name} ({device.address})")

    async with BleakClient(device) as client:
        # Проверка подключения
        if not client.is_connected:
            print("Не удалось подключиться к устройству.")
            return

        # Запись значения в характеристику
        await client.write_gatt_char(char_uuid, value)
        print(f"Значение {value} успешно записано в характеристику {char_uuid}.")

if __name__ == "__main__":
    service_uuid = "01942846-0661-7c4a-8953-e76f2ae2e6e2"
    char_uuid = "01942846-0761-7c4a-8953-e76f2ae2e6e2"
    value = "\x0D\x10\x11\x12\x13\x19\x1A\x1B\x0E\x15"
    data=(34812).to_bytes(2,byteorder='little')+b"pins\x00"+bytes(value, encoding="utf-8")+b"\x00"
    print(data)
    asyncio.run(find_and_write_to_device(service_uuid, char_uuid, data))