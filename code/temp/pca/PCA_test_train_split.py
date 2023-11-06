import os
import random

# Define the input files and the output files
data_file1 = "./PCA_Column/PCA_a.txt"
data_file2 = "./PCA_Column/PCA_b.txt"
labels_file = "./PCA_Labels/labels.txt"
train_data_file1 = "./Train_Test_Data/train_a.txt"
train_data_file2 = "./Train_Test_Data/train_b.txt"
train_labels_file = "./Train_Test_Data/train_labels.txt"
test_data_file1 = "./Train_Test_Data/test_a.txt"
test_data_file2 = "./Train_Test_Data/test_b.txt"
test_labels_file = "./Train_Test_Data/test_labels.txt"

output_directory = 'Train_Test_Data'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Open the input files and read the data and labels
with open(data_file1, 'r') as data_file1,open(data_file2, 'r') as data_file2, open(labels_file, 'r') as labels_file:
    data_lines1 = data_file1.readlines()
    data_lines2 = data_file2.readlines()
    label_lines = labels_file.readlines()

# Shuffle the data and labels randomly
combined_data = list(zip(data_lines1,data_lines2, label_lines))
random.shuffle(combined_data)

# Calculate the split point
total_lines = len(combined_data)
split_point = int(0.9 * total_lines)

# Split the data and labels into two lists
train_data1,train_data2, train_labels = zip(*combined_data[:split_point])
test_data1,test_data2, test_labels = zip(*combined_data[split_point:])

# Write the data and labels to the output files (create them if they don't exist)
with open(train_data_file1, 'w+') as file:
    file.writelines(train_data1)

with open(train_data_file2, 'w+') as file:
    file.writelines(train_data2)

with open(test_data_file1, 'w+') as file:
    file.writelines(test_data1)

with open(test_data_file2, 'w+') as file:
    file.writelines(test_data2)

# Write the labels to the output label files (create them if they don't exist)
with open(train_labels_file, 'w+') as file:
    file.writelines(train_labels)

with open(test_labels_file, 'w+') as file:
    file.writelines(test_labels)

print(f"Training data1 has been split into {len(train_data1)} lines for {train_data_file1} and {len(test_data1)} lines for {test_data_file1}.")
print(f"Training data2 has been split into {len(train_data2)} lines for {train_data_file2} and {len(test_data2)} lines for {test_data_file2}.")
print(f"Training labels have been split into {len(train_labels)} lines for {train_labels_file} and {len(test_labels)} lines for {test_labels_file}.")
