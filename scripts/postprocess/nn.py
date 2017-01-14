import numpy as np 
from sklearn.model_selection import train_test_split

def nonlin(x, deriv=False):  
    if(deriv==True):
        return (x*(1-x))
    
    return 1/(1+np.exp(-x)) 

def create_predictions():
	data=pd.read_csv('../../Projections/projections_NN.csv')
	dates=np.random.shuffle(dates)
	train_size=int(.7*len(dates))