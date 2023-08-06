import numpy as np
from dense import *
from loss import *
from metrics import *

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