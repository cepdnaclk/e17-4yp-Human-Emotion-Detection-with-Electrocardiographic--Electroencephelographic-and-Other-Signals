import csv
import os
import numpy as np

output_directory = 'EEG'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

separetor = " "

for i in range(23):
    for j in range(18):
        input_file = f'../DREAMER/EEG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv'

        original_data_lists = [list() for _ in range(14)]

        with open(input_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                for index, data_list in enumerate(original_data_lists):
                    data_list.append(row[index])

        for character, data_list in zip('abcdefghijklmn', original_data_lists):
            selected_data = data_list[-15360:]
            selected_data = np.array(selected_data)
            selected_data = np.array_split(selected_data, 60)
            final = []
            for k in range (60):
                data_string = separetor.join(selected_data[k])
                final.append(data_string)
            file_name = f'./{output_directory}/EEG_{character}.txt'
            with open(file_name, 'a') as textfile:
                    for line in final:
                        textfile.write(line + "\n")
