import numpy as np

class LrNeuralNetwork():

    def __init__(self, X, y):
        """stores predictive attributes and labels"""
        
        self.X = X
        self.y = y

        return None
    
    def sigmoid(self, z):
        '''compute the sigmoid of z'''
    
        s = 1 / (1 +  np.exp(-z))
        
        return s

    def initialize_with_zeros(self, dim):
        '''this function creates a vector of zeros of shape (dim, 1) for w and initializes b to 0'''
    
        w, b = np.zeros((dim, 1)), 0
        
        return w, b
    
    def propagate(self, w, b, X, Y):
        '''implement the cost function and its gradient for the propagation'''
    
        m = X.shape[1]
        A = self.sigmoid(np.dot(w.T, X) + b)
        cost = -1 / m * (np.sum(Y * np.log(A) + (1 - Y) * np.log(1 - A))) 
        dw = 1 / m * (np.dot(X, ((A - Y).T)))
        db = 1 / m * (np.sum(A - Y))
        cost = np.squeeze(cost)
        grads = {"dw": dw,
                "db": db}
        
        return grads, cost
    
    def optimize(self, w, b, X, Y, num_iterations, learning_rate, interval = 50, print_cost = False):
        '''this function optimizes w and b by running a gradient descent algorithm'''
        
        costs = []
        for i in range(num_iterations):
            grads, cost = self.propagate(w, b, X, Y)
            dw = grads["dw"]
            db = grads["db"]
            w = w - learning_rate * dw
            b = b - learning_rate * db
            if i % 100 == 0:
                costs.append(cost)
            if print_cost and i % interval == 0:
                print ("Cost after iteration %i: %f" %(i, cost))
        params = {"w": w,
                "b": b}
        grads = {"dw": dw,
                "db": db}
        
        return params, grads, costs
    
    def predict(self, w, b, X):
        '''predict whether the label is 0 or 1 using learned logistic regression parameters (w, b)'''

        m = X.shape[1]
        Y_prediction = np.zeros((1,m))
        w = w.reshape(X.shape[0], 1)
        A = self.sigmoid(np.dot(w.T, X)+ b)
        for i in range(A.shape[1]):
            Y_prediction[0][i] = 1 if A[0][i] > 0.5 else 0

        return Y_prediction

    def model(self, X_train, Y_train, X_test, Y_test, num_iterations = 2000, learning_rate = 0.5, interval = 50, print_cost = False):
        '''builds the logistic regression model by calling the function you've implemented previously'''
        
        w, b = self.initialize_with_zeros(X_train.shape[0])
        parameters, grads, costs = self.optimize(w, b, X_train, Y_train, num_iterations, learning_rate, interval, print_cost)
        w = parameters["w"]
        b = parameters["b"]
        Y_prediction_test = self.predict(w, b, X_test)
        Y_prediction_train = self.predict(w, b, X_train)
        print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
        print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))
        d = {"costs": costs,
            "Y_prediction_test": Y_prediction_test, 
            "Y_prediction_train" : Y_prediction_train, 
            "w" : w, 
            "b" : b,
            "learning_rate" : learning_rate,
            "num_iterations": num_iterations}
        
        return d