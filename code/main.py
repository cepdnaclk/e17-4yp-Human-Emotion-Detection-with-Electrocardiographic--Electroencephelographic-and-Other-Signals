import multiprocessing
import time


def task1():
    print("Task 1 started")
    time.sleep(2)  # Simulating some time-consuming task
    print("Task 1 finished")


def task2():
    print("Task 2 started")
    time.sleep(3)  # Simulating some time-consuming task
    print("Task 2 finished")


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=task1)
    process2 = multiprocessing.Process(target=task2)

    process1.start()
    process2.start()
    time.sleep(2.3)
    print("Hello World")

    process1.join()
    process2.join()

    print("All tasks completed")
