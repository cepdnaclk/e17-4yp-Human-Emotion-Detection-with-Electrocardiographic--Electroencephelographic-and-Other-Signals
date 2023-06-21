import multiprocessing
import time
from flask import Flask, request
from flask_cors import CORS

start = multiprocessing.Value('b', False)
processes = []  # to temporally maintain the running processes

app = Flask(__name__)
CORS(app)

def task1(request_data, start):

    x = 0
    print(start.value) 
    while start.value:
        time.sleep(5)
        x = x + 1
        print(x)

    print("writing to the file .....")


def task2():
    print("Task 2 running")
    time.sleep(5)
    print("Task 2 Finished")


@app.route("/", methods=['GET'])
def home():
    return "ECG/EEG signal receiver"


@app.route('/start', methods=['POST'])
def start_processes():
    global processes
    global start

    start.value = True  # to start the data collection process
    request_data = request.json

    if len(processes) == 0:
        process1 = multiprocessing.Process(target=task1, args=(request_data, start,))
        process2 = multiprocessing.Process(target=task2)
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
