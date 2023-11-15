import os
import numpy as np

DIVIDE_NUMBER = 1

label = [2, 1, 1, 4, 1, 4, 1, 4, 3, 4, 2, 1, 1, 4, 4, 1, 3, 1]
repeated_labels = np.repeat(label, DIVIDE_NUMBER)
output = np.tile(repeated_labels, 23)

output_directory = "Labels"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Create and open a text file for writing
with open('./Labels/labels.txt', 'w') as file:
    for element in output:
        file.write(str(element) + '\n')