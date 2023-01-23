import micropython
import neopixel
import machine 
import network
import web
import uasyncio as asyncio
import fsweb

app = web.App(host='0.0.0.0', port=80)

fsweb.init(app)

# Start event loop and create server task
loop = asyncio.get_event_loop()
loop.create_task(app.serve())
loop.run_forever()