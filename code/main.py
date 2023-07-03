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

skip = multiprocessing.Value('b', True)
start = multiprocessing.Value('b', False)
startFileWrite = multiprocessing.Value('b', False)
start_time = multiprocessing.Value('d', time.time())
participant_number = multiprocessing.Value('i', 0)
emotion = multiprocessing.Array('c', b' ' * 10)
start_datetime = multiprocessing.Array('c', b' ' * 20)

if not os.path.exists(SAVE_DIR_ECG):
    os.makedirs(SAVE_DIR_ECG)

if not os.path.exists(SAVE_DIR_EEG):
    os.makedirs(SAVE_DIR_EEG)

app = Flask(__name__)
CORS(app)


def ecg_collection(start, startFileWrite, start_time, start_datetime, participant_number, emotion,):
    COM_PORT_ECG = "COM12"
    BAUD_RATE = 115200

    data_points = []
    print("ECG process started")
    serialPortECG = serial.Serial(port=COM_PORT_ECG, baudrate=BAUD_RATE,
                                  bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

    print(serialPortECG)

    # print("Subject_" + str(participant_number) + " started")

    while start.value:
        while startFileWrite.value:
            if (serialPortECG.in_waiting > 0):
                # Read data out of the buffer until a new line is found
                serial_string = serialPortECG.readline()
                elapsed_time = time.time() - start_time.value

                try:
                    data_points.append(
                        str(format(elapsed_time, '.3f')) + ":" + str(serial_string.decode('Ascii').rstrip('\r\n')))
                except:
                    pass
        if len(data_points) > 0:
            print("writing to the file ECG")

            # make directory for subject id, emotion inside the SAVE_DIR
            if not os.path.exists(os.path.join(SAVE_DIR_ECG, str(participant_number.value))):
                os.makedirs(os.path.join(
                    SAVE_DIR_ECG, str(participant_number.value)))

            file_name = "ecg_" + str(participant_number.value) + "_" + \
                emotion.value.decode() + "_" + start_datetime.value.decode() + ".txt"
            with open((os.path.join(SAVE_DIR_ECG, str(participant_number.value), file_name)), 'w') as f:
                for line in data_points:
                    f.write(f"{line}\n")
            data_points = []

            print("file saved")


class Recording():

    def __init__(self, FIFO: multiprocessing.Queue, start, startFileWrite, start_time, start_datetime, participant_number, emotion, skip):
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
        self.start_datetime = start_datetime
        self.participant_number = participant_number
        self.emotion = emotion
        self.skip = skip

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

        if self.startFileWrite.value and not os.path.exists(os.path.join(SAVE_DIR_EEG, str(self.participant_number.value))):
            os.makedirs(os.path.join(
                SAVE_DIR_EEG, str(self.participant_number.value)))

        file_name = "eeg_" + str(self.participant_number.value) + "_" + \
            self.emotion.value.decode() + "_" + self.start_datetime.value.decode() + '.csv'

        if self.start.value and not self.startFileWrite.value and not os.path.exists(os.path.join(SAVE_DIR_EEG, str(
                self.participant_number.value), file_name)) and not self.skip.value:
            file = open((os.path.join(SAVE_DIR_EEG, str(
                self.participant_number.value), file_name)), "w")
            keys = "status, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7 \n"
            file.write(keys)

            print("File Opened For Write EEG")

            while 1:
                if self.FIFO.empty() == 0:
                    data = (str(self.FIFO.get())).split(',')
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
                    if (self.startFileWrite.value == False):
                        file.close()
                        print("File Closing EEG")
                        break
                    pass
            # print("EEG Process Terminated")

        if not self.start.value:
            self.FIFO.close()
            self.board.stop_stream()
            print("Closing Stream")

    def run(self):
        print('Starting Stream')
        self.board.start_stream(self.print_raw)


def eeg_collection(start, startFileWrite, start_time, start_datetime, participant_number, emotion, skip):
    print("EEG Process Started")
    FIFO = multiprocessing.Queue()

    recode = Recording(FIFO=FIFO, start=start,
                       startFileWrite=startFileWrite, start_time=start_time, start_datetime=start_datetime, participant_number=participant_number, emotion=emotion, skip=skip)
    recode.run()


@app.route("/")
def home():
    return "ECG & EEG data retriever"


@app.route('/start', methods=['POST'])
def start_processes():
    global processes
    global start
    global startFileWrite
    global start_time
    global start_datetime
    global participant_number
    global emotion

    start.value = True  # to start the data collection process

    if len(processes) == 0:
        process1 = multiprocessing.Process(target=ecg_collection, args=(
            start, startFileWrite, start_time, start_datetime, participant_number, emotion,))
        process2 = multiprocessing.Process(target=eeg_collection, args=(
            start, startFileWrite, start_time, start_datetime, participant_number, emotion, skip,))
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
    global participant_number
    global emotion
    global start_datetime
    global skip

    if start.value:
        request_data = request.json
        startFileWrite.value = True

        skip.value = False
        start_time.value = time.time()
        participant_number.value = int(request_data['subjectId'])
        emotion.value = request_data['emotion'].encode()
        start_datetime.value = str(datetime.datetime.now()).split('.')[
            0].replace(":", "_").encode()
        return "Started file write"
    else:
        return "Processes are not started yet"


@app.route('/stopWrite', methods=['POST'])
def stop_write():
    global startFileWrite

    if start.value:
        startFileWrite.value = False
        return "Stopped file write"
    else:
        return "Processes are not started yet"


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
