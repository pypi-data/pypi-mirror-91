import numpy as np 
from scipy import optimize

class LogisticRegression():

    def __init__(self, X, y):
        """stores predictive attributes and labels"""

        # predictive attributes
        self.X = X
        # values to be predicted
        self.y = y

        return None
    
    def sigmoid(self, z):
        '''compute sigmoid function given the input z'''

        z = np.array(z)
        g = np.zeros(z.shape)
        g = 1 / (1 + np.exp(-z))

        return g

    def cost_function(self, theta):
        '''compute cost and gradient for logistic regression'''

        m = self.y.size 
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        J = 0
        grad = np.zeros(theta.shape)
        h = self.sigmoid(X_bias.dot(theta.T))
        J = (1 / m) * np.sum(-self.y.dot(np.log(h)) - (1 - self.y).dot(np.log(1 - h)))
        grad = (1 / m) * (h - self.y).dot(X_bias)
        
        return J, grad

    def cost_function_reg(self, theta, X, y, lambda_):
        '''compute cost function for logistic regression with regularization'''

        m = len(y)
        J=(-1/m)*((y.T).dot(np.log(self.sigmoid(X.dot(theta))))+(1-y.T).dot(np.log(1-self.sigmoid(X.dot(theta)))))
        reg=(lambda_/(2*m))*((theta[1:].T).dot(theta[1:]))
        J += reg

        return J
    
    def gradient(self, theta, X, y, lambda_):
        '''compute gradient descent for logistic regression'''

        m = len(y)
        grad = np.zeros([m,1])
        grad = (1/m) * (X.T).dot((self.sigmoid(X.dot(theta)) - y))
        grad[1:] = grad[1:] + (lambda_ / m) * theta[1:]

        return grad

    def train_logistic_regression(self, theta, maxiter = 100):
        '''optimize the cost function with parameters theta'''

        options = {'maxiter': maxiter}
        res = optimize.minimize(self.cost_function, theta, jac=True, method='TNC', options=options)

        return res
    
    def train_logistic_regression_reg(self, X, y, lambda_, maxiter = 100):
        '''optimize the cost function with parameters theta'''
        
        theta = np.zeros(X.shape[1])
        options = {'maxiter': maxiter}
        output = optimize.fmin_tnc(func = self.cost_function_reg, 
                                   x0 = theta.flatten(), fprime = self.gradient, 
                                   args = (X, y.flatten(), lambda_))

        return output

    def predict(self, theta, Xtest, ytest):
        '''Predict whether the label is 0 or 1 using learned logistic regression.'''
        
        if (Xtest[:,0] != 1).all():
            m = Xtest.shape[0]
            Xtest = np.concatenate([np.ones((m, 1)), Xtest], axis=1)
        predict = self.sigmoid(np.dot(Xtest, theta)) >= 0.5
        
        return predict
    
    def map_feature(self, X1, X2, degree):
        '''maps the two input features to quadratic features used in the regularization'''

        if X1.ndim > 0:
            out = [np.ones(X1.shape[0])]
        else:
            out = [np.ones(1)]

        for i in range(1, degree + 1):
            for j in range(i + 1):
                out.append((X1 ** (i - j)) * (X2 ** j))

        if X1.ndim > 0:
            return np.stack(out, axis=1)
        else:
            return np.array(out, dtype=object)
        
        return None
    
    def validation_curve(self, X_poly, y, Xval, yval, lambda_vec):
        """analyzes the lambda values for the best normalization"""

        error_train = np.zeros(len(lambda_vec))
        error_val = np.zeros(len(lambda_vec))
        for i in range(len(lambda_vec)):
            lambda_try = lambda_vec[i]
            theta_t = self.train_logistic_regression_reg(X_poly, y, lambda_ = lambda_try)
            error_train[i] = self.cost_function_reg(theta_t[0], X_poly, y, lambda_ = 0)
            error_val[i] = self.cost_function_reg(theta_t[0], Xval, yval, lambda_ = 0)

        return error_train, error_val
    
    def learning_curve(self, X, y, Xval, yval, lambda_ = 0.0, maxiter = 200):
        """computes training error and validation error for different data extracts"""
        
        m = y.size
        error_train = np.zeros(m)
        error_val   = np.zeros(m)
        for i in range(1, m + 1):
            theta_t = self.train_logistic_regression_reg(X[:i], y[:i], lambda_, maxiter)
            error_train[i-1] = self.cost_function_reg(theta_t[0], X[:i], y[:i], lambda_)
            error_val[i - 1] = self.cost_function_reg(theta_t[0], Xval, yval, lambda_)
    
        return error_train, error_val


