from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import MaxPooling1D
from keras.models import Sequential
from keras.utils import to_categorical
from numpy import dstack
from numpy import mean
from numpy import std
from pandas import read_csv
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_model(trainX, trainy, testX, testy):
    verbose, epochs, batch_size = 0, 16, 32
    n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=4, activation='sigmoid', input_shape=(n_timesteps, n_features)))
    model.add(MaxPooling1D(pool_size=4))
    model.add(Conv1D(filters=64, kernel_size=4, activation='relu'))
    model.add(MaxPooling1D(pool_size=4))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(n_outputs, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit network
    # model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=1)
    # evaluate model
    # _, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
    # results = model.evaluate(testX, testy, batch_size=batch_size, verbose=1)
    # accuracy = results[model.metrics_names.index('accuracy')]
    # print("Accuracy:", accuracy)
    # predictions = model.predict(testX, batch_size=batch_size)
    # print("PREDICTIONS")
    # print(predictions)
    # predicted_labels = np.argmax(predictions, axis=1)
    # print("PREDICTED LABELS")
    # print(predicted_labels)
    # print("TEST_Y")
    # print(testy)
    # print("TEST_X")
    # print(testX)
    # conf_matrix = confusion_matrix(testy, predicted_labels)
    # print("Confusion Matrix:")
    # print(conf_matrix)
    # class_report = classification_report(testy, predicted_labels)
    # print("Classification Report:")
    # print(class_report)
    model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)

    # evaluate model on train set
    _, train_accuracy = model.evaluate(trainX, trainy, batch_size=batch_size, verbose=0)
    print('Train Accuracy: %.2f%%' % (train_accuracy * 100))

    # evaluate model on test set
    _, test_accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
    print('Test Accuracy: %.2f%%' % (test_accuracy * 100))

    return train_accuracy, test_accuracy

def load_file(filepath):
    dataFrame = read_csv(filepath, header=None, delim_whitespace=True)
    return dataFrame.values

def load_group(filenames, prefix=''):
    loaded = list()
    for name in filenames:
        data = load_file(prefix + name)
        loaded.append(data)
    # stack group so that features are the 3rd dimension
    loaded = dstack(loaded)
    return loaded

def load_dataset_group(group):
    filepath = './Train_Test_Spilt_ECG/'
    # load all 9 files as a single array
    filenames = list()
    filenames += [group + '_a.txt', group + '_b.txt']
    # load input data
    X = load_group(filenames, filepath)
    # load class output
    y = load_file(filepath + group + '_labels.txt')
    return X, y

def load_dataset():
    # load all train
    trainX, trainy = load_dataset_group('train')
    print(trainX.shape, trainy.shape)
    # load all test
    testX, testy = load_dataset_group('test')
    print(testX.shape, testy.shape)
    # zero-offset class values
    trainy = trainy - 1
    testy = testy - 1
    # one hot encode y
    trainy = to_categorical(trainy)
    testy = to_categorical(testy)
    print(trainX.shape, trainy.shape, testX.shape, testy.shape)
    return trainX, trainy, testX, testy

def summarize_results(scores):
    print(scores)
    m, s = mean(scores), std(scores)
    print('Accuracy: %.3f%% (+/-%.3f)' % (m, s))

def run_experiment(repeats=1):
    # load data
    trainX, trainy, testX, testy = load_dataset()
    print('Finished Loading the Data')
    # repeat experiment
    scores = list()
    for r in range(repeats):
        score = evaluate_model(trainX, trainy, testX, testy)
        score = score * 100.0
        print('>#%d: %.3f' % (r + 1, score))
        scores.append(score)
    # summarize results
    summarize_results(scores)

run_experiment()
