from flask import Flask, request
from flask_cors import CORS
import multiprocessing
import os
import datetime
import time
import serial
from pyOpenBCI_v1 import OpenBCICyton

COM_PORT_ECG = "COM3"
BAUD_RATE = 115200

SAVE_DIR_ECG = "DATA_FILES/ECG/"
SAVE_DIR_EEG = "DATA_FILES/EEG/"

processes = []  # to temporally maintain the running processes

start = multiprocessing.Value('b', False)

serialPortECG = serial.Serial(port=COM_PORT_ECG, baudrate=BAUD_RATE,
                              bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print(serialPortECG)

if not os.path.exists(SAVE_DIR_ECG):
    os.makedirs(SAVE_DIR_ECG)

if not os.path.exists(SAVE_DIR_EEG):
    os.makedirs(SAVE_DIR_EEG)

app = Flask(__name__)
CORS(app)


def ecg_collection(request_data, start, start_datetime, start_time, serialPort):

    data_points = []

    subject_id = str(request_data['subjectId'])
    emotion = str(request_data['emotion'])
    print("Subject_" + subject_id + " started")

    while start.value:
        if (serialPort.in_waiting > 0):
            # Read data out of the buffer until a new line is found
            serial_string = serialPort.readline()
            elapsed_time = time.time() - start_time

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

    def __init__(self, FIFO: multiprocessing.Queue, start):
        # create connection
        comPortEEG = 'COMX'  # provide Port for EEG
        self.board = OpenBCICyton(port=comPortEEG)
        print(self.board)
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

    def print_raw(self, sample):
        now = datetime.datetime.now()
        time = str(now.strftime("%M%S%f"))
        raw = (time + ',' + str(sample.channels_data[0])+',' +
               str(sample.channels_data[1])+',' +
               str(sample.channels_data[2])+',' +
               str(sample.channels_data[3])+',' +
               str(sample.channels_data[4])+',' +
               str(sample.channels_data[5])+',' +
               str(sample.channels_data[6])+',' +
               str(sample.channels_data[7]) + ' '
               )

        if self.start.value:
            self.FIFO.put(raw)

        if not self.start.value:
            self.FIFO.close()
            self.board.stop_stream()
            print("Closing Stream")

    def run(self):
        print('Starting Stream')
        self.board.start_stream(self.print_raw)

def recoding_call(FIFO: multiprocessing.Queue, start):
    recode = Recording(FIFO=FIFO, start=start)
    recode.run()

def eeg_collection(start):
    print("EEG Process Started")
    FIFO = multiprocessing.Queue()

    recode = multiprocessing.Process(target=recoding_call, args=(
        FIFO, start))
    recode.start()

    file = open_file_for_write()
    print("File Opened For Write EEG")
    while 1:
        if FIFO.empty() == 0:
            data = (str(FIFO.get())).split(',')
            tem = (data[1] + ',' +
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

    start.value = True  # to start the data collection process
    request_data = request.json

    if len(processes) == 0:
        start_datetime = str(datetime.datetime.now()).split('.')[
            0].replace(":", "_")
        start_time = time.time()
        process1 = multiprocessing.Process(target=ecg_collection, args=(
            request_data, start, start_datetime, start_time, serialPortECG,))
        process2 = multiprocessing.Process(
            target=eeg_collection, args=(start,))
        processes = [process1, process2]
        for process in processes:
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
            process.join()
        # we can use join or terminate according to the requirement
        processes = []
        return "Ended the processes."
    else:
        return "No processes are currently running."


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
