# Template Code for future references

from flask import Flask, request
import multiprocessing

app = Flask(__name__)
processes = []


def task1():
    while True:
        print("Task 1 running")
        # Add your task 1 logic here


def task2():
    while True:
        print("Task 2 running")
        # Add your task 2 logic here


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
            process.join()
        processes = []
        return "Ended the processes."
    else:
        return "No processes are currently running."


if __name__ == '__main__':
    app.run()
