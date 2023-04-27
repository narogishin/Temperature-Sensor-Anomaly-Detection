from flask import Flask, render_template, request
from flask_socketio import SocketIO
from utils.predict import Temperature_forecast, Humidity_forecast
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
thread_3 = None
thread_lock_3 = Lock()
thread_4 = None
thread_lock_4 = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins='*')

# s = socket.socket()
# s.bind(('IP_ADRESS', 5000))
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
        t = np.random.random() + 22
        info = {"date":get_current_datetime(), "temp":t}
        socketio.emit('updateSensorData', info)
        socketio.sleep(1)

def background_thread_2():
    print("Generating random sensor values")
    TIME = 1
    while True:
        pt = Temperature_forecast(TIME)
        info_2 = {"date":get_current_datetime(), "pred":round(pt, 5)}
        socketio.emit('P_updateSensorData', info_2)
        socketio.sleep(1)
        TIME += 1


def H_background_thread():
    print("Generating random sensor values")
    while True:
        h = np.random.random() + 22
        info = {"date":get_current_datetime(), "hum":h}
        socketio.emit('H_updateSensorData', info)
        socketio.sleep(1)

def H_background_thread_2():
    print("Generating random sensor values")
    TIME = 1
    while True:
        hpt = Humidity_forecast(TIME)
        info_2 = {"date":get_current_datetime(), "hum_pred":hpt}
        socketio.emit('PH_updateSensorData', info_2)
        socketio.sleep(1)
        TIME += 1
        

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
    print('Client connected')

    global thread
    global thread_2
    global thread_3
    global thread_4
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
            thread_2 = socketio.start_background_task(background_thread_2)
            thread_3 = socketio.start_background_task(H_background_thread)
            thread_4 = socketio.start_background_task(H_background_thread_2)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
    socketio.run(app)