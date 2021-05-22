import network
import web
import uasyncio as asyncio

# access point credentials
AP_SSID = 'SSE AP'
AP_PASSWORD = 'donthackmebro'
AP_AUTHMODE = network.AUTH_WPA_WPA2_PSK

app = web.App(host='0.0.0.0', port=80)

# root route handler
@app.route('/')
async def index_handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    w.write(b'''<html><head><script>
window.onload = () => {
    const out = document.querySelector('#out');
    const sse = new EventSource('/events');
    sse.onmessage = evt => {
        const el = document.createElement('div');
        el.innerText = evt.data;
        out.appendChild(el);
    };
};
</script></head>
<body><div id="out"></div></body></html>''')
    await w.drain()

# /events EventSource handler
@app.route('/events')
async def events_handler(r, w):
    # upgrade connection to EventSource (Server-Side Events)
    sse = await web.EventSource.upgrade(r, w)
    count = 0
    while True:
        count += 1
        try:
            await sse.send('Hello world #{}'.format(count))
        except:
            break
        await asyncio.sleep(1)

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
