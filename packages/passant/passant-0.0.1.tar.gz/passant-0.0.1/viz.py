import matplotlib.pyplot as plt
import numpy as np

def plotDataset(x, dataset, index=0, n=9):
    '''
    Function to visualize MNIST data set
    Parameters
    ----------
    x : multi-dimensional array
    index : integer
            plot figure i
    n : integer
        plot n figures 
    Returns
    -------
    None.
    '''
    num = range(index, index+n)
    counter=0
    if dataset is 'CIFAR10':
        for i in num:
            # define subplot
            plt.subplot(330 + 1 + counter)
            # reshape array and define rgb values
            im_r = x[i][0:1024].reshape(32, 32)
            im_g = x[i][1024:2048].reshape(32, 32)
            im_b = x[i][2048:].reshape(32, 32)
            # reconnect rgb arrays
            img = np.dstack((im_r, im_g, im_b))   
            # plot raw pixel data
            plt.imshow(img)
            # increment counter to draw multiple images in same plot
            counter = counter+1
    else:
        for i in num:
            # define subplot
            plt.subplot(330 + 1 + counter)
            im1 = x[i][0:784].reshape(28,28)
            # reshape image and plot raw pixel data
            plt.imshow(x[i].reshape(28,28), cmap=plt.get_cmap('gray'))
            # increment counter to draw multiple images in same plot
            counter = counter+1
    # show the figure
    plt.show()
    
    
def visualizeLoss(cost, ep):
    '''
    Function to visualize cost fn VS epochs
    Parameters
    ----------
    cost : 1D array

    Returns
    -------
    None.
    '''
    epochs = range(1,ep+1,1)
    plt.plot(epochs, cost, label='Training Loss')
    plt.title('Training loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.show()
    
def visualizeAccuracy(cost, ep):
    '''
    Function to visualize accuracy of cost fn VS epochs
    Parameters
    ----------
    cost : 1D array

    Returns
    -------
    None.
    '''
    epochs = range(1,ep+1,1)
    plt.plot(epochs, cost, label='Training accuracy')
    plt.title('Training Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()