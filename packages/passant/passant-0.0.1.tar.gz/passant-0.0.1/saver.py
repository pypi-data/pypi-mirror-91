import pickle

class saver():
    
    
    def save(data):
        # Store data (serialize)
        with open('model_MB_Momentum_LINAER-ACT.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("file saved")
            
    def restore():   
        # Load data (deserialize)
        with open('model_MB_Momentum_LINAER-ACT.pickle', 'rb') as handle:
            unserialized_data = pickle.load(handle)
            return unserialized_data


