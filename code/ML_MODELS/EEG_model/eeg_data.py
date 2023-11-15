import csv
import os

output_directory = 'EEG'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for i in range(23):
    for j in range(18):
        input_file = f'../DREAMER/EEG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv'

        original_data_lists = [list() for _ in range(14)]

        with open(input_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                for index, data_list in enumerate(original_data_lists):
                    # raw_data = float(row[index])  # Convert the string to a float
                    # rounded_data = round(raw_data, 6)  # Round to 6 decimal points
                    data_list.append(row[index])

        for character, data_list in zip('abcdefghijklmn', original_data_lists):
            selected_data = data_list[-15360:]
            data_string = " ".join(selected_data)
            file_name = f'./{output_directory}/EEG_{character}.txt'

            with open(file_name, 'a') as textfile:
                textfile.write(data_string + "\n")