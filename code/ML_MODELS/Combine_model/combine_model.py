from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Dropout, concatenate
from keras.layers import Flatten
from keras.layers import MaxPooling1D
from keras.models import Sequential
from keras.layers import Input
from keras.models import Model
from keras.utils import to_categorical
from numpy import dstack
from numpy import mean
from numpy import std
from pandas import read_csv


def evaluate_model(trainXEEG, trainXECG, trainy, testXEEG, testXECG, testy):
    verbose, epochs, batch_size = 0, 1, 32
    n_timesteps_EEG, n_features_EEG, n_outputs = trainXEEG.shape[1], trainXEEG.shape[2], trainy.shape[1]
    input_EEG = Input(shape=(n_timesteps_EEG, n_features_EEG))
    conv1_EEG = Conv1D(filters=64, kernel_size=3, activation='relu')(input_EEG)
    conv2_EEG = Conv1D(filters=64, kernel_size=3, activation='relu')(conv1_EEG)
    pool_EEG = MaxPooling1D(pool_size=2)(conv2_EEG)
    dropout_EEG = Dropout(0.5)(pool_EEG)
    flat_EEG = Flatten()(dropout_EEG)

    n_timesteps_ECG, n_features_ECG, n_outputs = trainXECG.shape[1], trainXECG.shape[2], trainy.shape[1]
    input_ECG = Input(shape=(n_timesteps_ECG, n_features_ECG))
    conv1_ECG = Conv1D(filters=64, kernel_size=3, activation='relu')(input_ECG)
    conv2_ECG = Conv1D(filters=64, kernel_size=3, activation='relu')(conv1_ECG)
    pool_ECG = MaxPooling1D(pool_size=2)(conv2_ECG)
    dropout_ECG = Dropout(0.5)(pool_ECG)
    flat_ECG = Flatten()(dropout_ECG)

    merged = concatenate([flat_EEG, flat_ECG])

    dense_layer = Dense(128, activation='relu')(merged)
    output = Dense(n_outputs, activation='softmax')(dense_layer)
    model = Model(inputs=[input_EEG, input_ECG], outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x=[trainXEEG, trainXECG], y=trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
    _, accuracy = model.evaluate(x=[testXEEG, testXECG], y=testy, batch_size=batch_size, verbose=0)
    return accuracy


def load_file(filepath):
    dataFrame = read_csv(filepath, header=None, delim_whitespace=True, engine='python')
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
    filepathEEG = './Train_Test_Data_EEG/'
    # load all 9 files as a single array
    filenames = list()
    filenames += [group + '_a.txt', group + '_b.txt']
    # load input data
    XEEG = load_group(filenames, filepathEEG)

    filepathECG = './Train_Test_Data_ECG/'
    # load all 9 files as a single array
    filenames = list()
    filenames += [group + '_a.txt', group + '_b.txt']
    # load input data
    XECG = load_group(filenames, filepathECG)

    # load class output
    y = load_file('./Train_Test_Data_EEG/' + group + '_labels.txt')
    return XEEG, XECG, y


def load_dataset():
    # load all train
    trainXEEG, trainXECG, trainy = load_dataset_group('train')
    print(trainXEEG.shape, trainXECG.shape, trainy.shape)
    # load all test
    testXEEG, testXECG , testy = load_dataset_group('test')
    print(testXEEG.shape, testXECG.shape, testy.shape)
    # zero-offset class values
    trainy = trainy - 1
    testy = testy - 1
    # one hot encode y
    trainy = to_categorical(trainy)
    testy = to_categorical(testy)
    print(trainXEEG.shape, trainXECG.shape, trainy.shape, testXEEG.shape, testXECG.shape, testy.shape)
    return trainXEEG, trainXECG, trainy, testXEEG, testXECG, testy


def summarize_results(scores):
    print(scores)
    m, s = mean(scores), std(scores)
    print('Accuracy: %.3f%% (+/-%.3f)' % (m, s))


def run_experiment(repeats=1):
    # load data
    trainXEEG, trainXECG, trainy, testXEEG, testXECG, testy = load_dataset()
    print('Finished Loading the Data')
    # repeat experiment
    scores = list()
    for r in range(repeats):
        score = evaluate_model(trainXEEG, trainXECG, trainy, testXEEG, testXECG, testy)
        score = score * 100.0
        print('>#%d: %.3f' % (r + 1, score))
        scores.append(score)
    # summarize results
    summarize_results(scores)


run_experiment()
