######                       defs                    ######

USERNAME = "Jacor4454"
WIFI_SSID = "JacorAP"
WIFI_PASSWORD = "Password123"




######                       setup section                    ######

import lvgl as lv

import machine
spi_bus = machine.SPI.Bus(host=1, mosi=13, sck=14)

import lcd_bus
display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=24_000_000, dc=2, cs=15)

import ili9341
display = ili9341.ILI9341(
     data_bus=display_bus,
     display_width=320,
     display_height=240,
     backlight_pin=21,
     backlight_on_state=ili9341.STATE_PWM,
     color_space=lv.COLOR_FORMAT.RGB565,
     color_byte_order=ili9341.BYTE_ORDER_RGB,
     rgb565_byte_swap=1
)
display.set_power(True)
display.init(1)
display._ORIENTATION_TABLE = (0xE0, 0x0, 0x0, 0x0)
display.set_rotation(lv.DISPLAY_ROTATION._0)
display.set_backlight(100)



######                       wifi section                    ######
import network
import time

NIC = None

# enable station interface and connect to WiFi access point
def connect():
    global WIFI_PASSWORD
    global WIFI_SSID
    global NIC

    print("connecting")
    NIC = network.WLAN(network.WLAN.IF_STA)
    NIC.active(True)
    NIC.connect(WIFI_SSID, WIFI_PASSWORD)
    while NIC.isconnected() == False:
        print('Waiting for connection..')
        time.sleep(1)
    print("connected")
    # now use sockets as usual

def disconnect():
    if NIC != None:
        NIC.disconnect()



######                     REST section                     ##########
import requests

def post(other : str):

    global USERNAME

    print("requesting")

    response = requests.get("http://api.jacobweb.co.uk/met", headers={"username":USERNAME, "other":other})

    # Get response code
    response_code = response.status_code
    print(response_code)


######                     ESPNow section                     ##########

import aioespnow
import asyncio

async def send_message(e, peer):
    while True:
        try:
            message = f"{USERNAME}"
            await e.asend(peer, message, sync=True)
            await asyncio.sleep(1)
        except OSError as err:
            print("ESPNow send encountered an issue:", err)
            await asyncio.sleep(5)
            
async def recv_message(e):
    met = set()
    while True:
        try:
            async for mac, msg in e:
                msg = msg.decode()
                print(f"Received from {mac.hex()}: {msg}")
                
                if not msg in met: 
                    met.add(msg)
                    post(msg)
                
        except OSError as err:
            print("ESPNow recv encountered an issue:", err)
            await asyncio.sleep(5)

async def esp_main(e, peer):
    await asyncio.gather(send_message(e, peer), recv_message(e))



######                     main section                     ##########

if __name__ == "__main__":
    import task_handler
    task_handler.TaskHandler()

    # connect to network
    connect()

    # start espnow
    print("starting async engine")

    e = aioespnow.AIOESPNow()
    e.active(True)

    unicast = b'\xff\xff\xff\xff\xff\xff'
    e.add_peer(unicast)

    asyncio.run(esp_main(e, unicast))

