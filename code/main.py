from flask import Flask, request
from flask_cors import CORS
import multiprocessing
import os
import datetime
import time
import serial
from pyOpenBCI_v1 import OpenBCICyton

SAVE_DIR_ECG = "DATA_FILES/ECG/"
SAVE_DIR_EEG = "DATA_FILES/EEG/"

processes = []  # to temporally maintain the running processes

start = multiprocessing.Value('b', False)
startFileWrite = multiprocessing.Value('b', False)
start_time = multiprocessing.Value('f', time.time())

if not os.path.exists(SAVE_DIR_ECG):
    os.makedirs(SAVE_DIR_ECG)

if not os.path.exists(SAVE_DIR_EEG):
    os.makedirs(SAVE_DIR_EEG)

app = Flask(__name__)
CORS(app)


def ecg_collection(request_data, start, startFileWrite, start_datetime, start_time):
    COM_PORT_ECG = "COM12"
    BAUD_RATE = 115200

    data_points = []
    serialPortECG = serial.Serial(port=COM_PORT_ECG, baudrate=BAUD_RATE,
                                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    print(serialPortECG)

    subject_id = str(request_data['subjectId'])
    emotion = str(request_data['emotion'])
    print("Subject_" + subject_id + " started")

    while start.value:
        if (serialPortECG.in_waiting > 0) and startFileWrite.value:
            # Read data out of the buffer until a new line is found
            serial_string = serialPortECG.readline()
            elapsed_time = time.time() - start_time.value

            try:
                data_points.append(
                    str(format(elapsed_time, '.3f')) + ":" + str(serial_string.decode('Ascii').rstrip('\r\n')))
            except:
                pass

    print("writing to the file ECG")

    # make directory for subject id, emotion inside the SAVE_DIR
    if not os.path.exists(os.path.join(SAVE_DIR_ECG, "S-" + subject_id)):
        os.makedirs(os.path.join(SAVE_DIR_ECG, "S-" + subject_id))

    if not os.path.exists(os.path.join(SAVE_DIR_ECG, "S-" + subject_id, emotion)):
        os.makedirs(os.path.join(SAVE_DIR_ECG, "S-" + subject_id, emotion))

    file_name = "S-" + subject_id + "_" + emotion + "_" + start_datetime + ".txt"
    with open((os.path.join(SAVE_DIR_ECG, "S-" + subject_id, emotion, file_name)), 'w') as f:
        for line in data_points:
            f.write(f"{line}\n")

    print("file saved")


def open_file_for_write():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
    file_name = SAVE_DIR_EEG + str(dt_string) + '.csv'

    file = open(file_name, "w")
    keys = "status, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7 \n"
    file.write(keys)
    return file


class Recording():

    def __init__(self, FIFO: multiprocessing.Queue, start, startFileWrite, start_time):
        self.board = OpenBCICyton()
        self.board.write_command('x1040010X')
        self.board.write_command('x2040010X')
        self.board.write_command('x3040010X')
        self.board.write_command('x4040010X')
        self.board.write_command('x5040010X')
        self.board.write_command('x6040010X')
        self.board.write_command('x7040010X')
        self.board.write_command('x8040010X')
        self.FIFO = FIFO
        self.start = start
        self.startFileWrite = startFileWrite
        self.start_time = start_time

    def print_raw(self, sample):
        elapsed_time = time.time() - self.start_time.value
        raw = (str(format(elapsed_time, '.3f')) + ',' + str(sample.channels_data[0])+',' +
               str(sample.channels_data[1])+',' +
               str(sample.channels_data[2])+',' +
               str(sample.channels_data[3])+',' +
               str(sample.channels_data[4])+',' +
               str(sample.channels_data[5])+',' +
               str(sample.channels_data[6])+',' +
               str(sample.channels_data[7]) + ' '
               )
        if self.start.value and self.startFileWrite.value:
            self.FIFO.put(raw)

        if not self.start.value:
            self.FIFO.close()
            self.board.stop_stream()
            print("Closing Stream")

    def run(self):
        print('Starting Stream')
        self.board.start_stream(self.print_raw)


def recoding_call(FIFO: multiprocessing.Queue, start, startFileWrite, start_time):
    recode = Recording(FIFO=FIFO, start=start,
                       startFileWrite=startFileWrite, start_time=start_time)
    recode.run()


def eeg_collection(start, startFileWrite, start_time):
    print("EEG Process Started")
    FIFO = multiprocessing.Queue()

    recode = multiprocessing.Process(target=recoding_call, args=(
        FIFO, start, startFileWrite, start_time,))
    recode.start()

    file = open_file_for_write()
    print("File Opened For Write EEG")
    while 1:
        if FIFO.empty() == 0:
            data = (str(FIFO.get())).split(',')
            tem = (data[0] + ',' +
                   data[1] + ',' +
                   data[2] + ',' +
                   data[3] + ',' +
                   data[4] + ',' +
                   data[5] + ',' +
                   data[6] + ',' +
                   data[7] + ',' +
                   data[8] + '\n')
            file.write(tem)
        else:
            if (start.value == False):
                file.close()
                recode.terminate()
                print("File Closing EEG")
                break
            pass
    print("EEG Process Terminated")


@app.route("/")
def home():
    return "ECG & EEG data retriever"


@app.route('/start', methods=['POST'])
def start_processes():
    global processes
    global start
    global startFileWrite
    global start_time

    start.value = True  # to start the data collection process
    request_data = request.json

    if len(processes) == 0:
        start_datetime = str(datetime.datetime.now()).split('.')[
            0].replace(":", "_")
        process1 = multiprocessing.Process(target=ecg_collection, args=(
            request_data, start, startFileWrite, start_datetime, start_time,))
        process2 = multiprocessing.Process(
            target=eeg_collection, args=(start, startFileWrite, start_time,))
        processes = [process1, process2]
        for process in processes:
            process.start()
        return "Started two new processes."
    else:
        return "Processes are already running."


@app.route('/startWrite', methods=['POST'])
def start_write():
    global start
    global startFileWrite
    global start_time

    if start.value:
        startFileWrite.value = True
        start_time.value = time.time()
    return "Started"


@app.route('/stop', methods=['POST'])
def end_processes():
    global processes
    global start

    start.value = False  # to stop the data collection process
    if len(processes) > 0:
        for process in processes:
            process.join()
        # we can use join or terminate according to the requirement
        processes = []
        return "Ended the processes."
    else:
        return "No processes are currently running."


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
