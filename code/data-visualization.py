import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

DATA_DIR = "/"

data = []
def read(file):
    print("reading ...")
    with open(file, 'r') as FP:
        for x in FP:
            values = x.split(':') 
            if (len(values) == 2 and (values[1].rstrip('\r\n'))!=''):
                data.append(int(values[1].rstrip('\r\n')))
        # data = [int() for x in FP]
    return data

ecg_signal = read('DATA_FILES/S-Test_Denuka_2/Happy/S-Test_Denuka_2_Happy_2023-06-21 22_40_20.txt')


figure(figsize=(10, 5), dpi=100)
plt.plot(ecg_signal, 'b')
plt.grid()
plt.title('Original ECG signal')
plt.tight_layout()
plt.show()

