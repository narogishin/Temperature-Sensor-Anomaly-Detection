from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
import socket
from threading import Lock
from datetime import datetime

"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

s = socket.socket()
s.bind(('192.168.155.172', 5000))
s.listen(0)

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Generating random sensor values")
    while True:
        client, addr = s.accept()

        content = client.recv(32*2)
        if len(content) == 0: continue

        h = content.decode('utf-8').split(",")[0]
        t = content.decode('utf-8').split(",")[1]
        print(t)
        info = {"date":get_current_datetime(), "temp":t}
        socketio.emit('updateSensorData', info)
        socketio.sleep(1)
        client.close()
        

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)