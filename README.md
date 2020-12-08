# micropython-aioweb
A very minimal asyncio web framework for MicroPython. Doesn't come with all the bells and whistles you might want out of a serious web framework but the goal is just to make asyncio HTTP applications in MicroPython as simple and efficient as possible.

## Current features
* minimal overhead in terms of code size or memory use
* easy integration into existing asyncio projects by running as a normal task alongside others
* basic endpoint/method based routing similar to flask (currently doesn't do any pattern matching)
* parses http request line, headers, and query strings
* supports WebSockets!

## Examples
### Basic "Hello world!"
```python
import web
import uasyncio as asyncio

app = web.App(host='0.0.0.0', port=80)

# root route handler
@app.route('/')
async def handler(r, w):
    # write http headers
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    # write page body
    w.write(b'Hello world!')
    # drain stream buffer
    await w.drain()

# Start event loop and create server task
loop = asyncio.get_event_loop()
loop.create_task(app.serve())
loop.run_forever()
```
### POST request handler
```python
@app.route('/', methods=['POST'])
async def handler(r, w):
    body = await r.read(1024)
    form = web.parse_qs(body.decode())
    name = form.get('name', 'world')
    # write http headers
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/html; charset=utf-8\r\n')
    w.write(b'\r\n')
    # write page body
    w.write(b'Hello {}!'.format(name))
    # drain stream buffer
    await w.drain()
```
### WebSocket handler
```python
# /ws WebSocket route handler
@app.route('/ws')
async def ws_handler(r, w):
    # upgrade connection to WebSocket
    ws = await WebSocket.upgrade(r, w)
    while True:
        evt = await ws.recv()
        if evt is None or evt['type'] == 'close':
            # handle closed stream/close event
            break
        elif evt['type'] == 'text':
            # print received messages and echo them
            print('Received:', evt['data'])
            await ws.send(evt['data'])
```
