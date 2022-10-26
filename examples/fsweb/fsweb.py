import uos
import web
import uasyncio as asyncio

async def status_handler(r, w):
    st = uos.statvfs("/")    
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/json; charset=utf-8\r\n')
    w.write(b'\r\n')
    json = "{\"type\":\"Filesystem\", \"isOk\":\"true\", \"totalBytes\":%i, \"usedBytes\":%i}" % (st[1]*st[2], st[1]*(st[2]-st[3]));
    w.write(json)
    await w.drain()

async def list_handler(r, w):
    w.write(b'HTTP/1.0 200 OK\r\n')
    w.write(b'Content-Type: text/json; charset=utf-8\r\n')
    w.write(b'\r\n')
    p = r.query.split("=")[1]
    l = uos.listdir(p)
    w.write("[")
    for i in range(len(l)):
        if i>0:
            w.write(",")
        stat = uos.stat(p+"/"+l[i])
        t = "dir" if (stat[0]==16384) else "file"
        w.write("{\"name\":\"%s\", \"type\":\"%s\", \"size\":%i}" % (l[i], t, stat[6]))
        await w.drain()
    w.write("]")
    await w.drain()       

async def root_handler(r, w):
    #if r.path=="/editor":
    #    r.path = "/editor/edit.htm.gz"
    #el
    if r.path=="/":
        r.path = "/index.htm"

    try:
        f = open(r.path, 'rb')
    except OSError:
        print(r.path)
        print(r.query)
        print(r.headers)
        w.write(b'HTTP/1.0 404 Not Found\r\n')
        await w.drain()
        return

    w.write(b'HTTP/1.0 200 OK\r\n')

    p = r.path
    if p.endswith(".gz"):
        w.write(b'Content-Encoding: gzip\r\n')
        p = p[0:-3]
    
    w.write(b'Content-Type:  ');
    if p.endswith(".htm") or p.endswith(".html"):
        w.write(b'text/html')
    elif p.endswith(".js"):
        w.write(b'application/javascript')
    elif p.endswith(".css"):
        w.write(b'text/css')
    elif p.endswith(".png"):
        w.write(b'image/png')
    else:
        w.write(b'text/plain')
    w.write(b'\r\n\r\n')

    l = f.read(1024)
    while (l):
        w.write(l)
        await w.drain()
        l = f.read(1024)
    f.close()

async def edit_post_handler(r, w):
    cl = int(r.headers["content-length"])
    ct = r.headers["content-type"].split("; ")
    if len(ct)==2 and ct[0]=="multipart/form-data":
        boundary = ct[1].split("=")[1]
        while True:
            await r.read(2); cl-=2
            bd = await r.read(len(boundary)); cl-=len(boundary)
            if (bd.decode()!=boundary):
                print("expected boundary")
                break
            bd = await r.read(2); cl-=2
            if bd.decode()=="--":
                bd = await r.read(2); cl-=2
                break
            fd = {}
            while True:
                cmd = await r.readline()
                cl-=len(cmd)                
                cmd = cmd[:-2].decode()
                if len(cmd)==0:
                    break                
                sc = cmd.split(": ")
                if sc[0]=="Content-Disposition":
                    for v in sc[1].split("; "):
                        v = v.split("=")
                        if len(v)==2:
                            fd[v[0]]=v[1][1:-1]                    
            print(fd)
            if r.method=="POST":        
                try:
                    sl = len(boundary) + 8
                    f = open(fd["filename"], 'wb')
                    while True:
                        body = await r.read(min(1024, cl-sl))
                        cl-=len(body)
                        f.write(body)
                        if cl==sl:
                            break
                    f.close()                    
                    bd = await r.read(2); cl-=2
                except OSError:
                    print("err saving")
            else:
                body = await r.readline()
                cl-=len(body)
                print(body[:-2].decode())
    if cl != 0:
        w.write(b'HTTP/1.0 500 Internal error\r\n')
    else:
        w.write(b'HTTP/1.0 200 OK\r\n')
        w.write(b'Content-Type: text/html; charset=utf-8\r\n')
        w.write(b'\r\n')
        w.write("caca")
    await w.drain()
    
async def edit_get_handler(r, w):
    if r.path=="/edit":
        r.path = "/edit/edit.htm.gz"
    await root_handler(r, w)    
    
def init(app):
    app.add_handler('/status', status_handler)
    app.add_handler('/list', list_handler)
    app.add_handler('/edit', edit_get_handler, methods=['GET'])
    app.add_handler('/edit', edit_post_handler, methods=['POST', "DELETE", "PUT"])
    app.add_handler('/', root_handler)
