import os
import csv
import numpy as np

DEVIDE_NUMBER = 1
Standardized = True
path = './Standardized_ECG/' if Standardized else '../DREAMER/ECG/'

for i in range (23):
    for j in range (18):
        with open(f'{path}{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            original_data_a = []
            original_data_b = []
            for row in csv_reader:
                original_data_a.append(row[0])
                original_data_b.append(row[1])

            output_directory = f'./ECG/'
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            selected_data_a = original_data_a[-15360:]
            selected_data_a = np.array(selected_data_a)
            selected_data_a = np.array_split(selected_data_a, DEVIDE_NUMBER)
            final_a = []
            for k in range (DEVIDE_NUMBER):
                data_string_a = " ".join(selected_data_a[k])
                final_a.append(data_string_a)
            with open(output_directory + 'ECG_a.txt', 'a') as textfile_a:
                for line in final_a:
                    textfile_a.write(line + "\n")

            selected_data_b = original_data_b[-15360:]
            selected_data_b = np.array(selected_data_b)
            selected_data_b = np.array_split(selected_data_b, DEVIDE_NUMBER)
            final_b = []
            for k in range (DEVIDE_NUMBER):
                data_string_b = " ".join(selected_data_b[k])
                final_b.append(data_string_b)
            with open(output_directory + 'ECG_b.txt', 'a') as textfile_b:
                for line in final_b:
                    textfile_b.write(line + "\n")