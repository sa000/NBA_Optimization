import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split

from numpy import exp, array, random, dot

class NeuralNetwork():
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.
        random.seed(1)

        # We model a single neuron, with 3 input connections and 1 output connection.
        # We assign random weights to a 3 x 1 matrix, with values in the range -1 to 1
        # and mean 0.
        self.synaptic_weights = 2 * random.random((7, 1)) - 1

    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # We train the neural network through a process of trial and error.
    # Adjusting the synaptic weights each time.
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in xrange(number_of_training_iterations):
            # Pass the training set through our neural network (a single neuron).
            output = self.think(training_set_inputs)

            # Calculate the error (The difference between the desired output
            # and the predicted output).
            error = training_set_outputs - output

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))

            # Adjust the weights.
            self.synaptic_weights += adjustment

    # The neural network thinks.
    def think(self, inputs):
        # Pass inputs through our neural network (our single neuron).
        return self.__sigmoid(dot(inputs, self.synaptic_weights))



def nonlin(x, deriv=False):  
    if(deriv==True):
        return (x*(1-x))
    
    return 1/(1+np.exp(-x)) 


  

data=pd.read_csv('../../Projections/projections_NN.csv')
dates=data['Date'].unique()
np.random.shuffle(dates)
train_size=int(.7*len(dates))
train_dates=dates[0:train_size]
test_dates=dates[train_size:]
#Features and output
numeric_data=pd.DataFrame(data, columns=['Date','Salary', 'Projected', 'Streak', 'last5', 'last3', 'last1', 'Salary Change'])
output_data=pd.DataFrame(data, columns=['Date', 'Scored'])

#Split
train_data=numeric_data[numeric_data['Date'].isin(train_dates)]
output_data_train=output_data[output_data['Date'].isin(train_dates)]

test_data=numeric_data[numeric_data['Date'].isin(test_dates)]
output_test_data=output_data[output_data['Date'].isin(test_dates)]

train_data=train_data.drop('Date', axis=1)
output_data_train=output_data_train.drop('Date', axis=1)

test_data=test_data.drop('Date', axis=1)
output_test_data=output_test_data.drop('Date',axis=1)
#Intialise a single neuron neural network.
neural_network = NeuralNetwork()

print "Random starting synaptic weights: "
print neural_network.synaptic_weights

# The training set. We have 4 examples, each consisting of 3 input values
# and 1 output value.
training_set_inputs = train_data.values
training_set_outputs = output_data_train.values

# Train the neural network using a training set.
# Do it 10,000 times and make small adjustments each time.
print 'output', training_set_outputs
neural_network.train(training_set_inputs, training_set_outputs, 10000)

print "New synaptic weights after training: "
print neural_network.synaptic_weights

# # Test the neural network with a new situation.
print "Considering new situation", test_data.shape
z=neural_network.think(test_data.values) 
print z, np.sum(z), len(z), test_data.shape, output_test_data.shape


