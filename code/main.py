import datetime
import multiprocessing
import os
import time

import serial
from flask import Flask, request
from flask_cors import CORS

COM_PORT = "COM3"
BAUD_RATE = 115200

SAVE_DIR = "DATA_FILES/"

subject_id = ""
emotion = ""
start_datetime = ""
data_points = []
start_time = ""

start = multiprocessing.Value('b', False)

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

app = Flask(__name__)
CORS(app)

# Uncomment following when the data collection is connected to the port
# serialPort = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
# print(serialPort)

serial_string = ""  # To hold data coming over UART
processes = []  # to temporally maintain the running processes


def ecg_collection(request_data, start):

    global data_points
    # global subject_id
    # global emotion
    global start_datetime
    global start_time
    global serial_string  # I have added this

    print("Task 1.1 running")
    time.sleep(2)
    print("Task 1.1 Finished")

    start_time = time.time()
    subject_id = str(request_data['subjectId'])
    emotion = str(request_data['emotion'])

    print(subject_id)
    time.sleep(2)
    print(emotion)
    serialPort = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    print(serialPort)
    print("start: " + str(start.value))
    while start.value:
        print("Started")
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a new line is found
            serial_string = serialPort.readline()
            elapsed_time = time.time() - start_time

            try:
                data_points.append(
                    str(format(elapsed_time, '.3f')) + ":" + str(serial_string.decode('Ascii').rstrip('\r\n')))
            except:
                pass

        start_datetime = str(datetime.datetime.now()).split('.')[0].replace(":", "_")

        print("Subject_" + subject_id + " started")

        return "Subject-" + subject_id + " started"

    print("writing to the file .....")
    # print(subject_id)

    # make directory for subject id, emotion inside the SAVE_DIR
    if not os.path.exists(os.path.join(SAVE_DIR, "S-" + subject_id)):
        os.makedirs(os.path.join(SAVE_DIR, "S-" + subject_id))

    if not os.path.exists(os.path.join(SAVE_DIR, "S-" + subject_id, emotion)):
        os.makedirs(os.path.join(SAVE_DIR, "S-" + subject_id, emotion))

    file_name = "S-" + subject_id + "_" + emotion + "_" + start_datetime + ".txt"
    with open((os.path.join(SAVE_DIR, "S-" + subject_id, emotion, file_name)), 'w') as f:
        for line in data_points:
            f.write(f"{line}\n")

    data_points = []
    serial_string = ""
    print("file saved")


def task2():
    print("Task 2 running")
    time.sleep(3)
    print("Task 2 Finished")


@app.route("/")
def home():
    return "ECG Serial Communication server!"


@app.route('/start', methods=['POST'])
def start_processes():
    global processes
    global start

    start.value = True  # to start the data collection process
    request_data = request.json

    if len(processes) == 0:
        process1 = multiprocessing.Process(target=ecg_collection, args=(request_data, start,))
        process2 = multiprocessing.Process(target=task2)
        processes = [process1, process2]
        for process in processes:
            print("start init: " + str(start.value))
            process.start()
        return "Started two new processes."
    else:
        return "Processes are already running."


@app.route('/stop', methods=['POST'])
def end_processes():
    global processes
    global start

    start.value = False  # to stop the data collection process
    if len(processes) > 0:
        for process in processes:
            # process.terminate()
            process.join()
        # we can use join or terminate according to the requirement
        processes = []
        return "Ended the processes."
    else:
        return "No processes are currently running."


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
