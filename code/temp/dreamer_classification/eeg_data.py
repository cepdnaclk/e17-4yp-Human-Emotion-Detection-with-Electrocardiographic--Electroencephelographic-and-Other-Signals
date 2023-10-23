import csv

for i in range(23):
    for j in range(18):
        input_file = f'./DREAMER/EEG/{i+1}/{j+1}/{i+1}_{j+1}_stimuli.csv'

        original_data_lists = [list() for _ in range(14)]

        with open(input_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                for index, data_list in enumerate(original_data_lists):
                    data_list.append(row[index])

        for character, data_list in zip('abcdefghijklmnn', original_data_lists):
            data_string = " ".join(data_list)
            file_name = f'EEG_{character}.txt'

            with open(file_name, 'a') as textfile:
                textfile.write(data_string + "\n")
