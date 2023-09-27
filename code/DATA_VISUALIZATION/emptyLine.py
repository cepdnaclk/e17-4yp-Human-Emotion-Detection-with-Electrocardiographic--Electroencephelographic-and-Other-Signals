# Specify the file name
file_name = '../DATA_ACQUSITION_BACKEND/DATA_FILES/ECG/1006/ecg_1006_NEUTRAL_2023-09-26 15_28_39.txt'

# Read the lines from the file and filter out empty lines
with open(file_name, 'r') as file:
    lines = file.readlines()
    lines = [line for line in lines if line.strip()]

# Write the non-empty lines back to the same file
with open(file_name, 'w') as file:
    file.writelines(lines)
