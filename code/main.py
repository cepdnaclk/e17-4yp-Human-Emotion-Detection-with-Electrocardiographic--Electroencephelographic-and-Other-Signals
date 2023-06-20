import multiprocessing
import time
from flask import Flask, request
import serial
import continuous_threading
import os
import datetime
from flask_cors import CORS

COM_PORT = "COM3"
BAUD_RATE = 115200

SAVE_DIR = "DATA_FILES/"

subject_id = ""
emotion = ""
start_datetime = ""
data_points = []
start_time = ""

start = False
save_file = False

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

app = Flask(__name__)
CORS(app)

# serialPort = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
# print(serialPort)
serial_string = ""  # To hold data coming over UART

processes = []


def task1():
    while True:
        print("Task 1 running")
        time.sleep(2)
        print("Task 1 Finished")


def task2():
    while True:
        print("Task 2 running")
        time.sleep(3)
        print("Task 2 Finished")


@app.route("/")
def home():
    return "ECG Serial Communication server!"


@app.route('/start', methods=['POST'])
def start_processes():
    global processes
    if len(processes) == 0:
        process1 = multiprocessing.Process(target=task1)
        process2 = multiprocessing.Process(target=task2)
        processes = [process1, process2]
        for process in processes:
            process.start()
        return "Started two new processes."
    else:
        return "Processes are already running."


@app.route('/end', methods=['POST'])
def end_processes():
    global processes
    if len(processes) > 0:
        for process in processes:
            process.terminate()
            # process.join()
        # we can use this if we want to finish the process
        processes = []
        return "Ended the processes."
    else:
        return "No processes are currently running."


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
