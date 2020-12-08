import network
import web
import uasyncio as asyncio

# access point credentials
AP_SSID = 'Hello AP'
AP_PASSWORD = 'donthackmebro'
AP_AUTHMODE = network.AUTH_WPA_WPA2_PSK

app = web.App(host='0.0.0.0', port=80)

# root route handler
@app.route('/')
async def handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    w.write(b'Hello world!')
    await w.drain()

# Create WiFi access point
wifi = network.WLAN(network.AP_IF)
wifi.active(True)
wifi.config(essid=AP_SSID, password=AP_PASSWORD, authmode=AP_AUTHMODE)
while wifi.active() == False:
    pass
print(wifi.ifconfig())

# Start event loop and create server task
loop = asyncio.get_event_loop()
loop.create_task(app.serve())
loop.run_forever()
