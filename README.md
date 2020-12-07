# micropython-aioweb
A very minimal asyncio web framework for MicroPython. Doesn't come with all the bells and whistles you might want out of a serious web framework but the goal is just to make asyncio HTTP applications in MicroPython as simple and efficient as possible.

## Current features:
* minimal overhead in terms of code size or memory use
* easy integration into existing asyncio projects by running as a normal task alongside others
* basic endpoint/method based routing similar to flask (currently doesn't do any pattern matching)
* parses http request line, headers, and query strings
* supports WebSockets!
