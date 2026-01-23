import asyncio
import sys
from bleak import BleakClient, BleakScanner

service_uuid = "01942846-0661-7c4a-8953-e76f2ae2e6e2"
char_uuid = "01942846-0761-7c4a-8953-e76f2ae2e6e2"

# 0.2.0 базовая версия с самодельной платой зарядки
# 0.2.1 версия с моторами с другим порядком проводов
# 0.2.2 версия с ESP32 с 4 МБайт памяти (а не с 8)
# 0.3.1 распространенная версия с smd разъемами и перепаянным разъемом на заводской плате питания

pins = {
    "0.2.0":"\x0D\x10\x11\x12\x13\x19\x1A\x1B\x0E\x15", #Version 0.2.0 pins
    "0.2.1":"\x0D\x10\x11\x12\x13\x19\x0E\x1B\x1A\x15", #Version 0.2.1 pins
    "0.2.2":"\x0D\x19\x0E\x1B\x1A\x10\x11\x12\x13\x15", #Version 0.2.2 pins
    "0.3.1":"\x0D\x13\x12\x11\x10\x0E\x1B\x1A\x19\x15", #Version 0.3.1 pins
}
async def find_and_write_to_device(hw):
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
        # Прочитать версию из устройства
        if hw is None:
            try:
                hw=(await client.read_gatt_char("2A27")).decode()
            except Exception as e:
                print(e)
        if hw is None:
            print("Не удалось прочитать версию устройства. Укажите ее явно: python RePin.py <version>")
            return
        value=pins.get(hw)
        if value is None:
            print(f"Неизвестная версия устройства: {hw}")
            return
        print(f"Версия устройства: {hw}")
        data=(34812).to_bytes(2,byteorder='little')+b"pins\x00"+bytes(value, encoding="utf-8")+b"\x00"
        # Запись значения в характеристику
        try:
            await client.write_gatt_char(char_uuid, data)
            print(f"Значение {data} успешно записано в характеристику {char_uuid}.")
        except Exception as e:
            print(e)
            print("Не удалось записать")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        value=None
    else:
        value=sys.argv[1]

#    data=(34812).to_bytes(2,byteorder='little')+b"pins\x00"+bytes(value, encoding="utf-8")+b"\x00"
    asyncio.run(find_and_write_to_device(value))