import network
import web
import uasyncio as asyncio

# access point credentials
AP_SSID = 'WebSocket AP'
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
    const form = document.querySelector('form');
    const input = document.querySelector('#msg');
    const socket = new WebSocket('ws://192.168.4.1/ws');
    socket.onmessage = evt => {
        const el = document.createElement('div');
        el.innerText = evt.data;
        out.insertBefore(el, out.firstChild);
    };
    form.onsubmit = evt => {
        evt.preventDefault();
        socket.send(msg.value);
        msg.value = '';
    };
};
</script></head>
<body>
<form><input id="msg" autofocus autocomplete="off"></form>
<div id="out"></div>
</body></html>''')
    await w.drain()

# Store current WebSocket clients
WS_CLIENTS = set()

# /ws WebSocket route handler
@app.route('/ws')
async def ws_handler(r, w):
    global WS_CLIENTS
    # upgrade connection to WebSocket
    ws = await web.WebSocket.upgrade(r, w)
    # add current client to set
    WS_CLIENTS.add(ws)
    while True:
        # handle ws events
        evt = await ws.recv()
        if evt is None or evt['type'] == 'close':
            break
        elif evt['type'] == 'text':
            # echo received message to all clients
            for ws_client in WS_CLIENTS:
                try:
                    await ws_client.send(evt['data'])
                except:
                    continue
    # remove current client from set
    WS_CLIENTS.discard(ws)

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
