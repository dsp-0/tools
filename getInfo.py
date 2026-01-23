import asyncio
import sys
from bleak import BleakClient, BleakScanner

async def find_and_write_to_device(service_uuid, char_uuid):
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
#        print("Сервисы")
#        for s in client.services:
#            print(s.uuid,s.description)
#        print("Характеристики")
#        for n,ch in client.services.characteristics.items():
#            print(n,ch.uuid,ch.description)
        model=b""
        fw=b""
        hw=b""
        try:
            model=await client.read_gatt_char("2A24")
            fw=await client.read_gatt_char("2A26")
            hw=await client.read_gatt_char("2A27")
        except Exception as e:
            print(e)
        model=model.decode()
        fw=fw.decode()
        hw=hw.decode()

        print(f"Модель: {model}\nВерсия устройства: {hw}\nВерсия прошивки: {fw}")

if __name__ == "__main__":
    service_uuid = "01942846-0661-7c4a-8953-e76f2ae2e6e2"
    char_uuid = "01942846-0761-7c4a-8953-e76f2ae2e6e2"
    asyncio.run(find_and_write_to_device(service_uuid, char_uuid))