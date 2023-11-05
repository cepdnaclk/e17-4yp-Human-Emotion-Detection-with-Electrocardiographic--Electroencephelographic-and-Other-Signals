import numpy as np

label = [2, 1, 1, 4, 1, 4, 1, 4, 3, 4, 2, 1, 1, 4, 4, 1, 3, 1]
repeated_labels = np.tile(label, 23)

# Create and open a text file for writing
with open('./PCA_Labels/labels.txt', 'w') as file:
    for element in repeated_labels:
        file.write(str(element) + '\n')