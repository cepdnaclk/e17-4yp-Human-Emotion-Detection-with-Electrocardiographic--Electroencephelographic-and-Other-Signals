import random

# Define the input files and the output files
output_files = []
input_files = []
train_files = []
test_files = []
characters = 'abcdefghijklmn'

for char in characters:
    input_files.append(f"EEG_{char}.txt")
    output_files.append(f"output_{char}.txt")
    train_files.append(f"train_{char}.txt")
    test_files.append(f"test_{char}.txt")

labels_file = "labels.txt"
train_labels_file = "train_labels.txt"
test_labels_file = "test_labels.txt"

# Read the data and labels from the input files
data_lines = {}
for char, input_file in zip(characters, input_files):
    with open(input_file, 'r') as data_file:
        data_lines[char] = data_file.readlines()

with open(labels_file, 'r') as labels_file:
    label_lines = labels_file.readlines()

# Shuffle the data and labels randomly
combined_data = list(zip(*[data_lines[char] for char in characters], label_lines))
random.shuffle(combined_data)

# Calculate the split point
total_lines = len(combined_data)
split_point = int(0.9 * total_lines)

# Split the data and labels and write them to the output files (create them if they don't exist)
for char in characters:
    train_data = combined_data[:split_point]
    test_data = combined_data[split_point:]

    with open(train_files[characters.index(char)], 'w+') as file:
        file.writelines(train_data)

    with open(test_files[characters.index(char)], 'w+') as file:
        file.writelines(test_data)

# Split the labels and write them to the output label files (create them if they don't exist)
train_labels, test_labels = zip(*combined_data[:split_point], *combined_data[split_point:])
with open(train_labels_file, 'w+') as file:
    file.writelines(train_labels)

with open(test_labels_file, 'w+') as file:
    file.writelines(test_labels)

for char in characters:
    print(
        f"Training data for {char} has been split into {len(train_data)} lines for {train_files[characters.index(char)]} and {len(test_data)} lines for {test_files[characters.index(char)]}.")

print(
    f"Training labels have been split into {len(train_labels)} lines for {train_labels_file} and {len(test_labels)} lines for {test_labels_file}.")
