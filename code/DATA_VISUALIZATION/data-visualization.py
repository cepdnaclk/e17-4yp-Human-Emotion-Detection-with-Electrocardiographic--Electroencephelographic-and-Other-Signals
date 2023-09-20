import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

DATA_DIR = "/"

data = []


def read(file):
    print("reading ...")
    with open(file, 'r') as FP:
        for x in FP:
            # values = x.split(',')
            # if (len(values) == 2 and (values[0].rstrip('\r\n')) != ''):
            data.append(int(x.rstrip('\r\n')))
        # data = [int() for x in FP]
    return data


ecg_signal = read(
    '../DATA_ACQUSITION_BACKEND/DATA_FILES/ECG/19405/ecg_19405_HAPPY_2023-09-20 15_57_10.txt')

figure(figsize=(10, 5), dpi=100)
plt.plot(ecg_signal, 'b')
plt.grid()
plt.title('Original ECG signal')
plt.tight_layout()
plt.show()
