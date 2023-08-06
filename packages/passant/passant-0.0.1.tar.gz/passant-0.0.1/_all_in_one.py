import numpy as np
from actvfn import *
from Preprocessing import *
from loss import *
from viz import *
from metrics import *
from saver import *

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
    

class layer:
    def __init__(self, output_dims, input_dims, act_fn):
        self.weights = np.random.randn(output_dims, input_dims) #* np.sqrt(2/input_dims)
        self.biases = np.zeros((output_dims,1))
        self.act_fn = act_fn
        self.Z = None
        self.A = None
        
        self.dW = np.zeros((output_dims, input_dims))
        self.db = np.zeros((output_dims,1))
        self.dZ = None
        self.dA = None
        self.v_w = np.random.randn(output_dims, input_dims)
        self.v_b = np.zeros((output_dims,1))
        
    def forward_prop(self, input):
        self.Z = np.dot(self.weights, input) + self.biases
        
        if self.act_fn == "sigmoid":
            self.A = sigmoid(self.Z)
        if self.act_fn == "relu":
            self.A = relu(self.Z)
        if self.act_fn == "tanh":
            self.A = tanh(self.Z)
        if self.act_fn == "linear":
            self.A = linear(self.Z)
        if self.act_fn == "softmax":
            self.A = softmax(self.Z)
            
        return self.A
        
    def backward_prop(self, prev_A, dA_prev, y, output_layer = False):
        if output_layer is True:
            self.dZ = self.A - y
            self.dW = (1./y.shape[1]) * np.dot(self.dZ, prev_A.T)
            self.db = (1./y.shape[1]) * np.sum(self.dZ, axis=1, keepdims=True)
            dA_prev = np.dot(self.weights.T, self.dZ)
               
        else:
            if self.act_fn == "sigmoid":
                self.dZ = dA_prev * derivative_sigmoid(self.Z)
            elif self.act_fn == "tanh":
                self.dZ = dA_prev * derivative_tanh(self.Z)
            elif self.act_fn == "relu":
                self.dZ = dA_prev * d_relu(self.Z)
            elif self.act_fn == "linear":
                self.dZ = dA_prev * d_linear(self.Z)
                
            self.dW = (1./y.shape[1]) * np.dot(self.dZ, prev_A.T)
            self.db = (1./y.shape[1]) * np.sum(self.dZ, axis=1, keepdims=True)
            dA_prev = np.dot(self.weights.T, self.dZ)
            
        return dA_prev
    
    def update_parameters(self, learning_rate):
        self.weights = self.weights -  learning_rate * self.dW
        self.biases= self.biases -  learning_rate * self.db

    def update_parameters_momentum(self, learning_rate, gamma=0.9):
        self.v_w = gamma*self.v_w + learning_rate*self.dW
        self.v_b = gamma*self.v_b + learning_rate*self.db
        self.weights -= self.v_w
        self.biases -= self.v_b


class Model:
    def __init__(self, layers_dims, activation_fns):
        self.layers = []
        self.num_of_layers = len(layers_dims)

        for i in range(1, self.num_of_layers):
            self.layers.append(layer(layers_dims[i], layers_dims[i-1], activation_fns[i-1]))
        
        self.loss = None
        
    def predict(self, X):
        output = X
        for layer in self.layers:
            output = layer.forward_prop(output)

        _pred = np.array(output[0])        
        pred = np.zeros((10,X.shape[1]))  
        pred = np.argmax(output,axis=0)
        
        return np.atleast_2d(pred)
        
    def predict_ext_image(self, path):
        px = Image.open(path)     
        gray_image = ImageOps.grayscale(px)    
        new_image = gray_image.resize((28, 28))   
        #   new_image = gray_image
        new_image.show()
        
        pix_val = np.array(list(new_image.getdata()))    
        pix_val =np.atleast_2d(pix_val)
        pix_val = pix_val/255
        pred = model.predict(pix_val)
        print(pred)
    
    def fit(self, X, y, learning_rate, metrics, epochs, batch_size, costt, use_momentum):
        y_class = np.zeros((10,y.shape[1]))  
        y_class = np.atleast_2d(np.argmax(y,axis=0))
        batch_number = int(-(-X.shape[1]/batch_size // 1))
        accuracy = []
        loss = []
        
        for i in range(epochs):
            for j in range(batch_number):
                if j == batch_number:
                        
                    output = X[:,batch_size*(j):]
                    A = []
                    A.append(output)
                    for layer in self.layers:
                        output = layer.forward_prop(output)
                        A.append(output)                
                    
                    if (costt == "multiclass"):
                        self.loss = compute_multiclass_loss(y[:,batch_size*(j):], output)
                    elif (costt == "mse"):
                        self.loss = compute_mse_loss(y[:,batch_size*(j):], output)
                        
                    output_layer = True
                    dA_prev = 0
                    k = self.num_of_layers - 1
                    for layer in reversed(self.layers):
                        dA_prev = layer.backward_prop(A[k - 1], dA_prev, y[:,batch_size*(j):], output_layer)
                        output_layer = False
                        k = k - 1
                    
                    if use_momentum:
                        for layer in self.layers:
                            layer.update_parameters_momentum(learning_rate)
                    else:
                        for layer in self.layers:
                            layer.update_parameters(learning_rate)
                         
                         
                else:
                    
                    output = X[:,batch_size*(j):batch_size*(j+1)]
                    A = []
                    A.append(output)
                    for layer in self.layers:
                        output = layer.forward_prop(output)
                        A.append(output)                
                    
                    if (costt == "multiclass"):
                        self.loss = compute_multiclass_loss(y[:,batch_size*(j):batch_size*(j+1)], output)
                    elif (costt == "mse"):
                        self.loss = compute_mse_loss(y[:,batch_size*(j):batch_size*(j+1)], output)
                        
                    output_layer = True
                    dA_prev = 0
                    k = self.num_of_layers - 1
                    for layer in reversed(self.layers):
                        dA_prev = layer.backward_prop(A[k - 1], dA_prev, y[:,batch_size*(j):batch_size*(j+1)], output_layer)
                        output_layer = False
                        k = k - 1
                        
                    if use_momentum:
                        for layer in self.layers:
                            layer.update_parameters_momentum(learning_rate)
                    else:
                        for layer in self.layers:
                            layer.update_parameters(learning_rate)
                        
            print("Epoch", i, "->")
            print("\t\tLoss =", ("%.4f" % self.loss ))
            loss.append(self.loss)
            pred = self.predict(X)
            
            for j in range(len(metrics)):
                if metrics[j] == "accuracy":
                    acc = accuracy_metrics(pred.T, y_class.T) * 100
                    accuracy.append(acc) 
                    print("\t\tAccuracy =", ("%.4f" % acc ))
                # elif metrics[j] == "confusion matrix":
                #     conf = confusion_matrix(pred.T, y_class.T) * 100
                #     print("\t\tConfusion matrix =", ("%.4f" % conf ))
                elif metrics[j] == "absolute metrics":
                    abso = absolute_metrics(pred.T, y_class.T) * 100
                    print("\t\tAbsolute metrics =", ("%.4f" % abso ))
                elif metrics[j] == "F1 score":
                     f1 = F1_score(pred.T, y_class.T) * 100
                     print("\t\tF1 score =", ("%.4f" % f1 ))
                    
                
        print("\n___________________________________________________\n")
        print("Final cost:", ("%.5f" % self.loss ))
        
        for j in range(len(metrics)):
                if metrics[j] == "accuracy":
                    print("Final training accuracy:", ("%.5f" % acc ), "%")
                # elif metrics[j] == "confusion matrix":
                #     print("Final training value for confusion matrix:", ("%.5f" % conf ), "%")
                elif metrics[j] == "absolute metrics":
                    print("Final training value for absolute metrics:", ("%.5f" % abso ), "%")
                elif metrics[j] == "F1 score":
                     print("Final training value for F1 score:", ("%.5f" % f1 ), "%")
        
        return loss, accuracy
            

trainFeatures, trainLabels, testFeatures, testLabels, Dataset = preprocessing(r'D:\4th CSE\Neural Networks\Project\MNISTcsv')

trainLabels = labels_to_onehot(trainLabels)

X = trainFeatures.T
Y = trainLabels
layers_dims = [X.shape[0], 128, 10]
activation_fns = ["sigmoid", "softmax"]
batch_size = 30
epochs = 20
learning_rate = 0.005
costt = "multiclass"
metrics = ["accuracy", "F1 score", "absolute metrics"]
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

