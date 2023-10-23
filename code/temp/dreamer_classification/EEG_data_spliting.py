import random

# Define the input files and the output files
data_file1 = "EEG_a.txt"
data_file2 = "EEG_b.txt"
data_file3 = "EEG_c.txt"
data_file4 = "EEG_d.txt"
data_file5 = "EEG_e.txt"
data_file6 = "EEG_f.txt"
data_file7 = "EEG_g.txt"
data_file8 = "EEG_h.txt"
data_file9 = "EEG_i.txt"
data_file10 = "EEG_j.txt"
data_file11 = "EEG_k.txt"
data_file12 = "EEG_l.txt"
data_file13 = "EEG_m.txt"
data_file14 = "EEG_n.txt"

labels_file = "labels.txt"

train_data_file1 = "train_a.txt"
train_data_file2 = "train_b.txt"
train_data_file3 = "train_c.txt"
train_data_file4 = "train_d.txt"
train_data_file5 = "train_e.txt"
train_data_file6 = "train_f.txt"
train_data_file7 = "train_g.txt"
train_data_file8 = "train_h.txt"
train_data_file9 = "train_i.txt"
train_data_file10 = "train_j.txt"
train_data_file11 = "train_k.txt"
train_data_file12 = "train_l.txt"
train_data_file13 = "train_m.txt"
train_data_file14 = "train_n.txt"

train_labels_file = "train_labels.txt"

test_data_file1 = "test_a.txt"
test_data_file2 = "test_b.txt"
test_data_file3 = "test_c.txt"
test_data_file4 = "test_d.txt"
test_data_file5 = "test_e.txt"
test_data_file6 = "test_f.txt"
test_data_file7 = "test_g.txt"
test_data_file8 = "test_h.txt"
test_data_file9 = "test_i.txt"
test_data_file10 = "test_j.txt"
test_data_file11 = "test_k.txt"
test_data_file12 = "test_l.txt"
test_data_file13 = "test_m.txt"
test_data_file14 = "test_n.txt"

test_labels_file = "test_labels.txt"

# Open the input files and read the data and labels
with open(data_file1, 'r') as data_file1,open(data_file2, 'r') as data_file2,open(data_file3, 'r') as data_file3,open(data_file4, 'r') as data_file4,open(data_file5, 'r') as data_file5,open(data_file6, 'r') as data_file6,open(data_file7, 'r') as data_file7,open(data_file8, 'r') as data_file8,open(data_file9, 'r') as data_file9,open(data_file10, 'r') as data_file10,open(data_file11, 'r') as data_file11,open(data_file12, 'r') as data_file12,open(data_file13, 'r') as data_file13,open(data_file14, 'r') as data_file14,open(labels_file, 'r') as labels_file:
    data_lines1 = data_file1.readlines()
    data_lines2 = data_file2.readlines()
    data_lines3 = data_file3.readlines()
    data_lines4 = data_file4.readlines()
    data_lines5 = data_file5.readlines()
    data_lines6 = data_file6.readlines()
    data_lines7 = data_file7.readlines()
    data_lines8 = data_file8.readlines()
    data_lines9 = data_file9.readlines()
    data_lines10 = data_file10.readlines()
    data_lines11 = data_file11.readlines()
    data_lines12 = data_file12.readlines()
    data_lines13 = data_file13.readlines()
    data_lines14 = data_file14.readlines()
    label_lines = labels_file.readlines()

# Shuffle the data and labels randomly
combined_data = list(zip(data_lines1,data_lines2,data_lines3,data_lines4,data_lines5,data_lines6,data_lines7,data_lines8,data_lines9,data_lines10,data_lines11,data_lines12,data_lines13,data_lines14,label_lines))
random.shuffle(combined_data)

# Calculate the split point
total_lines = len(combined_data)
split_point = int(0.9 * total_lines)

# Split the data and labels into two lists
train_data1,train_data2,train_data3,train_data4,train_data5,train_data6,train_data7,train_data8,train_data9,train_data10,train_data11,train_data12,train_data13,train_data14,train_labels = zip(*combined_data[:split_point])
test_data1,test_data2,test_data3,test_data4,test_data5,test_data6,test_data7,test_data8,test_data9,test_data10,test_data11,test_data12,test_data13,test_data14,test_labels = zip(*combined_data[split_point:])

# Write the data and labels to the output files (create them if they don't exist)
with open(train_data_file1, 'w+') as file:
    file.writelines(train_data1)

with open(train_data_file2, 'w+') as file:
    file.writelines(train_data2)

with open(train_data_file3, 'w+') as file:
    file.writelines(train_data3)

with open(train_data_file4, 'w+') as file:
    file.writelines(train_data4)

with open(train_data_file5, 'w+') as file:
    file.writelines(train_data5)

with open(train_data_file6, 'w+') as file:
    file.writelines(train_data6)

with open(train_data_file7, 'w+') as file:
    file.writelines(train_data7)

with open(train_data_file8, 'w+') as file:
    file.writelines(train_data8)

with open(train_data_file9, 'w+') as file:
    file.writelines(train_data9)

with open(train_data_file10, 'w+') as file:
    file.writelines(train_data10)

with open(train_data_file11, 'w+') as file:
    file.writelines(train_data11)

with open(train_data_file12, 'w+') as file:
    file.writelines(train_data12)

with open(train_data_file13, 'w+') as file:
    file.writelines(train_data13)

with open(train_data_file14, 'w+') as file:
    file.writelines(train_data14)

with open(test_data_file1, 'w+') as file:
    file.writelines(test_data1)

with open(test_data_file2, 'w+') as file:
    file.writelines(test_data2)

with open(test_data_file3, 'w+') as file:
    file.writelines(test_data3)

with open(test_data_file4, 'w+') as file:
    file.writelines(test_data4)

with open(test_data_file5, 'w+') as file:
    file.writelines(test_data5)

with open(test_data_file6, 'w+') as file:
    file.writelines(test_data6)

with open(test_data_file7, 'w+') as file:
    file.writelines(test_data7)

with open(test_data_file8, 'w+') as file:
    file.writelines(test_data8)

with open(test_data_file9, 'w+') as file:
    file.writelines(test_data9)

with open(test_data_file10, 'w+') as file:
    file.writelines(test_data10)

with open(test_data_file11, 'w+') as file:
    file.writelines(test_data11)

with open(test_data_file12, 'w+') as file:
    file.writelines(test_data12)

with open(test_data_file13, 'w+') as file:
    file.writelines(test_data13)

with open(test_data_file14, 'w+') as file:
    file.writelines(test_data14)

# Write the labels to the output label files (create them if they don't exist)
with open(train_labels_file, 'w+') as file:
    file.writelines(train_labels)

with open(test_labels_file, 'w+') as file:
    file.writelines(test_labels)

print(f"Training data1 has been split into {len(train_data1)} lines for {train_data_file1} and {len(test_data1)} lines for {test_data_file1}.")
print(f"Training data2 has been split into {len(train_data2)} lines for {train_data_file2} and {len(test_data2)} lines for {test_data_file2}.")
print(f"Training labels have been split into {len(train_labels)} lines for {train_labels_file} and {len(test_labels)} lines for {test_labels_file}.")
