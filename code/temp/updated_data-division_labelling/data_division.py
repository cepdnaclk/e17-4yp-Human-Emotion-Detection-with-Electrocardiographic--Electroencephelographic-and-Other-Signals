import os
import csv
import numpy as np

for i in range (23):
    for j in range (18):
        with open(f'./PCA_EEG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            original_data_a = []
            original_data_b = []
            for row in csv_reader:
                original_data_a.append(row[0])
                original_data_b.append(row[1])

            output_directory = 'PCA_Column'
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            separator = ' '
              
            selected_data_a = original_data_a[-15360:]
            selected_data_a = np.array(selected_data_a)
            selected_data_a = np.array_split(selected_data_a, 60)
            final_a = []
            for k in range (60):
                data_string_a = separator.join(selected_data_a[k])
                final_a.append(data_string_a)
            with open('PCA_Column/PCA_a.txt', 'a') as textfile_a:
                for final in final_a:
                    textfile_a.write(final + "\n")

            selected_data_b = original_data_b[-15360:]
            selected_data_b = np.array(selected_data_b)
            selected_data_b = np.array_split(selected_data_b, 60)
            final_b = []
            for l in range (60):
                data_string_b = separator.join(selected_data_b[l])
                final_b.append(data_string_b)
            with open('PCA_Column/PCA_b.txt', 'a') as textfile_b:
                for final in final_b:
                    textfile_b.write(final + "\n")