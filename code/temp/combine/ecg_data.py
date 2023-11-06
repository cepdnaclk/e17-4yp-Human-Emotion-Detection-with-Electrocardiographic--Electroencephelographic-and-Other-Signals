import os 
import csv

for i in range (23):
    for j in range (18):
        with open(f'../dreamer_classification/DREAMER/ECG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv', 'r') as csvfile:
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
            data_string_a = " ".join(selected_data_a)
            with open(output_directory + 'ECG_a.txt', 'a') as textfile_a:
                textfile_a.write(data_string_a + "\n")

            selected_data_b = original_data_b[-15360:]
            data_string_b = " ".join(selected_data_b)
            with open(output_directory + 'ECG_b.txt', 'a') as textfile_b:
                textfile_b.write(data_string_b + "\n")