from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
import numpy as np
import socket
from threading import Lock
from datetime import datetime

"""
Background Thread
"""
thread = None
thread_lock = Lock()
thread_2 = None
thread_lock_2 = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

# s = socket.socket()
# s.bind(('192.168.155.172', 5000))
# s.listen(0)

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
        t = random()
        info = {"date":get_current_datetime(), "temp":t}
        socketio.emit('updateSensorData', info)
        socketio.sleep(1)


def background_thread_2():
    print("Generating random sensor values")
    while True:
        p = np.random.rand() +10
        info_2 = {"date":get_current_datetime(), "pred":p}
        socketio.emit('P_updateSensorData', info_2)
        socketio.sleep(1)
        

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
    global thread_2
    print('Client connected')

    global thread
    global thread_2
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
            thread_2 = socketio.start_background_task(background_thread_2)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)