from model import *
from Preprocessing import *
from viz import *


def main():
    trainFeatures, trainLabels, testFeatures, testLabels, Dataset = preprocessing(r'D:\Gam3a\Neural\Project\Datasets\MNIST')
    trainLabels = labels_to_onehot(trainLabels)

    
    X = trainFeatures.T
    Y = trainLabels
    layers_dims = [X.shape[0], 128, 10]
    activation_fns = ["sigmoid", "softmax"]
    batch_size = 30
    epochs = 20
    learning_rate = 0.1
    costt = "multiclass"
    metrics = ["accuracy"]
    use_momentum = False
    
    plotDataset(trainFeatures, Dataset)

    model = Model(layers_dims, activation_fns)
    loss_train, acc_train = model.fit(X, Y, learning_rate, metrics, epochs, batch_size, costt, use_momentum)
    
    visualizeLoss(loss_train, epochs)
    visualizeAccuracy(acc_train, epochs)
    
    # saver.save(parameters)
    # parameters_new = saver.restore()
    
    pred = model.predict(testFeatures.T)
    accuracy = accuracy_metrics(pred.T, testLabels.T) * 100
    print(f"\nThe accuracy rate of TEST DATASET is: {accuracy:.2f}%.")
    
if __name__ == "__main__":
    main()
