from fastapi import FastAPI
import socketio
from uvicorn import Config, Server
import threading
import asyncio

app = FastAPI()
sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

connected_clients = {}

@app.get("/")
def handle_start():
    return { "status_code": 200, "message": "This is the first route"}

@sio.on("connect")
async def handle_connect(sid, environ):
    connected_clients[sid] = environ
    print("CONNECTED TO THE SERVER")

async def send_commands():
    while True:
        command = input("Enter the command to send to the socket: \n")
        print("sending command: {}".format(command))
        if command.lower() == "exit":
            break
        for sid in connected_clients.keys():
            await sio.emit("command", { "command": command }, room=sid)

@sio.on("disconnect")
async def handle_disconnect(sid):
    print("CLIENT DISCONNECTED FROM THE SERVER")
    if sid in connected_clients.keys():
        del connected_clients[sid]
    else:
        print("CLIENT sid: {} not found among the connected clients".format(sid))
    

@app.on_event("startup")
async def handle_startup():
    print("SERVER STARTED RUNNING")
    def handle_event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_commands())
        loop.close()
    while_loop_event = threading.Thread(target=handle_event_loop)
    while_loop_event.start()

@app.on_event("shutdown")
async def handle_shutdown():
    print("SERVER SHUTDOWN RUNNING")

if __name__ == "__main__":
    config = Config(app, host='127.0.0.1', port=5000, reload=True)
    server = Server(config=config)
    server.run()
    
        
        


    
    
