import numpy as np
import pandas as pd
import os
import pickle

def preprocessing(path):

    #path = r'D:\Gam3a\Neural\Project\Datasets\CIFAR-10\cifar-10-batches-py'
    data_directory_path = path
    filenames = os.listdir(data_directory_path)

    #For CIFAR Dataset:

    if 'csv' not in filenames[0]:

        trainLabels = []
        trainFeatures = []
        Dataset = 'CIFAR10'
        for file in filenames:
            if '_batch' in file:
                with open(path+'/'+file, 'rb') as fo:
                    dict = pickle.load(fo, encoding='bytes')
                    if 'test' in file:
                        testLabels = dict[b'labels']
                        testFeatures = dict[b'data']
                    else:
                        trainLabels.append(dict[b'labels'])
                        trainFeatures.append(dict[b'data'])

        trainLabels = np.array(trainLabels)
        trainFeatures = np.array(trainFeatures)
        trainLabels = trainLabels.reshape((-1,1))
        trainFeatures = trainFeatures.reshape((-1,3072))
        testLabels = np.array(testLabels)
        testLabels =np.atleast_2d(testLabels)
        trainLabels =np.atleast_2d(trainLabels.T)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
        

    #For MNIST Dataset:

    else:
        trainData = pd.read_csv(path+'/train.csv')
        testData = pd.read_csv(path+'/test.csv')
        trainData = np.array(trainData)
        testData = np.array(testData)
        trainLabels = np.array(trainData[:,0])
        trainFeatures = np.array(trainData[:,1:])
        testFeatures = np.array(testData[:,1:])
        testLabels = np.array(testData[:,0])  
        testLabels =np.atleast_2d(testLabels)
        trainLabels =np.atleast_2d(trainLabels.T)
        trainFeatures = trainFeatures/255
        testFeatures = testFeatures/255 
        idx = np.random.permutation(len(trainFeatures))
        trainFeatures = trainFeatures[idx]
        TrainLabels = trainLabels.T[idx]
        trainLabels = TrainLabels.T
        Dataset = 'MNIST'
        
    return trainFeatures, trainLabels, testFeatures, testLabels, Dataset



def labels_to_onehot(labels):
    max = np.max(labels)
    enc = np.zeros((max+1,labels.shape[1]))
    for i in range(labels.shape[1]):
        for j in range(max):
            enc[j][i] = (labels[0][i] == j)  ###hot encoding trainLabels
            if (labels[0][i] == 9):
                enc[9][i] = 1
    onehot_labels = enc
    
    return onehot_labels



#'D:\Gam3a\Neural\Project\Datasets\CIFAR-10\cifar-10-batches-py'
