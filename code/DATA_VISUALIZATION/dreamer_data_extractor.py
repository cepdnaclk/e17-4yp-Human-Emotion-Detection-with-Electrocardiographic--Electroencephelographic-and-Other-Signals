import scipy.io
import numpy as np
import csv
import re
import os

def clean_data(data):
    cleaned_data = re.sub(r'[\[\]\']', '', data)
    return cleaned_data

def clean_csv(file_name):
    cleaned_data = []
    with open(file_name, 'r', newline='') as input_file:
        csv_reader = csv.reader(input_file)
    
        for row in csv_reader:
            cleaned_row = [clean_data(cell) for cell in row]
            cleaned_data.append(cleaned_row)

    with open(file_name, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)

        for cleaned_row in cleaned_data:
            csv_writer.writerow(cleaned_row)

mat_data = scipy.io.loadmat('DREAMER.mat')
dreamer_data = mat_data['DREAMER']
dreamer_data = dreamer_data[0][0]
structure = dreamer_data.dtype
# print(structure)
ECG_SamplingRate = (dreamer_data['ECG_SamplingRate'])[0][0]
EEG_SamplingRate = (dreamer_data['EEG_SamplingRate'])[0][0]
EEG_Electrodes = (dreamer_data['EEG_Electrodes'])[0]
noOfSubjects = (dreamer_data['noOfSubjects'])[0][0]
noOfVideoSequences = (dreamer_data['noOfVideoSequences'])[0][0]
data = (dreamer_data['Data'])[0]
print(f'ECG_SamplingRate\t: {ECG_SamplingRate}')
print(f'EEG_SamplingRate\t: {EEG_SamplingRate}')
print(f'EEG_Electrodes\t\t: {len(EEG_Electrodes)}')
print(f'noOfSubjects\t\t: {noOfSubjects}')
print(f'noOfVideoSequences\t: {noOfVideoSequences}')
np.savetxt('eeg_electrodes.csv', EEG_Electrodes, delimiter=',', fmt='%s')
clean_csv('eeg_electrodes.csv')

# participants_data = []
# for participant_details in data:
#     participant_data = []
#     participant_data.append(participant_details['Age'][0][0])
#     participant_data.append(participant_details['Gender'][0][0])
#     participants_data.append(participant_data)

# with open('participant_data.csv', 'w', newline='') as output_file:
#         csv_writer = csv.writer(output_file)

#         for cleaned_row in participants_data:
#             csv_writer.writerow(cleaned_row)

# print(data[0].dtype)
# clean_csv('participant_data.csv')

# user_id = 0
# for participant_details in data:
#     user_id = user_id + 1
#     path = os.path.join(os.getcwd(), 'ECG', f'{user_id}')
#     if not os.path.exists(path):
#         os.makedirs(path)
#     ECG = participant_details['ECG'][0][0]
#     baseline = ECG['baseline'][0][0]
#     stimuli_id = 0
#     for sample in baseline:
#         stimuli_id = stimuli_id + 1
#         path = os.path.join(os.getcwd(), 'ECG', f'{user_id}', f'{stimuli_id}')
#         if not os.path.exists(path):
#             os.makedirs(path)
#         np.savetxt(f'./ECG/{user_id}/{stimuli_id}/{user_id}_{stimuli_id}_baseline.csv', sample[0], delimiter=',', fmt='%s')

# user_id = 0
# for participant_details in data:
#     user_id = user_id + 1
#     path = os.path.join(os.getcwd(), 'ECG', f'{user_id}')
#     if not os.path.exists(path):
#         os.makedirs(path)
#     ECG = participant_details['ECG'][0][0]
#     stimuli = ECG['stimuli'][0][0]
#     stimuli_id = 0
#     for sample in stimuli:
#         stimuli_id = stimuli_id + 1
#         path = os.path.join(os.getcwd(), 'ECG', f'{user_id}', f'{stimuli_id}')
#         if not os.path.exists(path):
#             os.makedirs(path)
#         np.savetxt(f'./ECG/{user_id}/{stimuli_id}/{user_id}_{stimuli_id}_stimuli.csv', sample[0], delimiter=',', fmt='%s')

# user_id = 0
# for participant_details in data:
#     user_id = user_id + 1
#     path = os.path.join(os.getcwd(), 'EEG', f'{user_id}')
#     if not os.path.exists(path):
#         os.makedirs(path)
#     EEG = participant_details['EEG'][0][0]
#     baseline = EEG['baseline'][0][0]
#     stimuli_id = 0
#     for sample in baseline:
#         stimuli_id = stimuli_id + 1
#         path = os.path.join(os.getcwd(), 'EEG', f'{user_id}', f'{stimuli_id}')
#         if not os.path.exists(path):
#             os.makedirs(path)
#         np.savetxt(f'./EEG/{user_id}/{stimuli_id}/{user_id}_{stimuli_id}_baseline.csv', sample[0], delimiter=',', fmt='%s')

# user_id = 0
# for participant_details in data:
#     user_id = user_id + 1
#     path = os.path.join(os.getcwd(), 'EEG', f'{user_id}')
#     if not os.path.exists(path):
#         os.makedirs(path)
#     EEG = participant_details['EEG'][0][0]
#     stimuli = EEG['stimuli'][0][0]
#     stimuli_id = 0
#     for sample in stimuli:
#         stimuli_id = stimuli_id + 1
#         path = os.path.join(os.getcwd(), 'EEG', f'{user_id}', f'{stimuli_id}')
#         if not os.path.exists(path):
#             os.makedirs(path)
#         np.savetxt(f'./EEG/{user_id}/{stimuli_id}/{user_id}_{stimuli_id}_stimuli.csv', sample[0], delimiter=',', fmt='%s')

# user_id = 0
# for participant_details in data:
#     user_id = user_id + 1
#     path = os.path.join(os.getcwd(), 'Emotion')
#     if not os.path.exists(path):
#         os.makedirs(path)
#     ScoreValence = participant_details['ScoreValence'][0][0]
#     ScoreArousal = participant_details['ScoreArousal'][0][0]
#     stimuli_id = 0
#     emotions = []
#     for i in range (18):
#         valance = ScoreValence[i][0]
#         arousal = ScoreArousal[i][0]
#         emotion = [valance, arousal]
#         emotions.append(emotion)

#     with open(f'./Emotion/{user_id}_valance_arousal.csv', 'w', newline='') as output_file:
#         csv_writer = csv.writer(output_file)

#         for cleaned_row in emotions:
#             csv_writer.writerow(cleaned_row)