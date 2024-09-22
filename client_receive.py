import socketio

host = "http://127.0.0.1:5000"

# Create a Socket.IO client instance
sio = socketio.Client()

@sio.event
def connect():
    print("CONNECTED TO THE SERVER")

@sio.on('command')  # Listen for the 'command' event
def handle_command(data):
    print("Received command data: {}".format(data))

@sio.event
def disconnect():
    print("Disconnected from the server")

if __name__ == '__main__':
    print("Started")
    try:
        sio.connect(host)
        sio.wait()  # Keep the connection alive to wait for events
    except Exception as e:
        print(f"Connection failed: {e}")
