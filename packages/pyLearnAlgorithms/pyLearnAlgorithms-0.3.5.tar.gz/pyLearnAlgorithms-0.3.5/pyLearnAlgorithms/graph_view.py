from matplotlib import pyplot as plt
import numpy as np
from pyLearnAlgorithms.linear_regression import LinearRegression
from pyLearnAlgorithms.polynomial_regression import PolynomialRegression
from pyLearnAlgorithms.logistic_regression import LogisticRegression
from pyLearnAlgorithms.lr_neural_network import LrNeuralNetwork

class GraphView():
    """graphic display class of machine learning models"""

    def __init__(self, X = np.array([]), y = np.array([])):
        """stores predictive attributes and labels"""

        self.X = X
        self.y = y
    
        return None

    def view_data(self, xlabel, ylabel, title):
        """data visualization"""

        plt.figure(figsize = (10, 5))
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        return None

    def view_data_labels(self, labels, xlabel, ylabel, title, legends = []):
        '''function to plot classified data'''
        
        fig = plt.figure(figsize = (10, 5))
        plt.plot(self.X[labels[0], 0], self.X[labels[0], 1], 'k*', lw=2, ms=10)
        plt.plot(self.X[labels[1], 0], self.X[labels[1], 1], 'ko', mfc='y', ms=8, mec='k', mew=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(legends)
                
        return None

    def model_linear(self, xlabel, ylabel, title, theta):
        """plots the graph of the linear regression model"""

        m = self.y.size 
        plt.figure(figsize = (10,5))
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1.5)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.plot(self.X, np.dot(X_bias, theta), '--', lw=2)

        return None

    def model_linear_normal_equation(self, xlabel, ylabel, title, theta):
        """plots the graph of the linear regression model with normal equation"""

        m = self.y.size 
        plt.figure(figsize = (10,5))
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1.5)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.plot(self.X, np.dot(X_bias, theta), '--', lw=2)

        return None
    
    def model_poly(self, xlabel, ylabel, title, theta, poly_degree, mu, sigma, lambda_ = 0.0, maxiter = 200):
        """plots the graph of the polynomial regression model"""

        x = np.arange(np.min(self.X) - 15, np.max(self.X) + 25, 0.05).reshape(-1, 1)
        model_poly = PolynomialRegression(self.X, self.y)
        xpoly = model_poly.poly_features(x, poly_degree)
        xpoly -= mu
        xpoly /= sigma
        xpoly = np.concatenate([np.ones((x.shape[0], 1)), xpoly], axis=1)
        plt.figure(figsize = (10, 5))
        plt.plot(self.X, self.y, 'ro', ms=10, mew=1.5, mec='k')
        plt.plot(x, np.dot(xpoly, theta), '--', lw=2)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        #plt.ylim([np.min(self.y) - 15, np.max(self.y) + 25])
        
        return None
    
    def model_logistic(self, X, degree, labels, theta, xlabel, ylabel, title, legends = []):
        '''plots the classifier's decision boundary'''

        self.view_data_labels(labels, xlabel, ylabel, title, legends)
        theta = np.array(theta)

        if X.shape[1] <= 3:
            plot_x = np.array([np.min(X[:, 1]) - 2, np.max(X[:, 1]) + 2])
            plot_y = (-1. / theta[2]) * (theta[1] * plot_x + theta[0])
            plt.plot(plot_x, plot_y)
            plt.legend(legends)
            plt.xlim([30, 100])
            plt.ylim([30, 100])
        else:
            model = LogisticRegression(self.X, self.y)
            u = np.linspace(-1, 1.5, 50)
            v = np.linspace(-1, 1.5, 50)
            z = np.zeros((u.size, v.size))
            for i, ui in enumerate(u):
                for j, vj in enumerate(v):
                    z[i, j] = np.dot(model.map_feature(ui, vj, degree), theta)
            z = z.T  
            plt.contour(u, v, z, levels=[0], linewidths=2, colors='g')
            plt.contourf(u, v, z, levels=[np.min(z), 0, np.max(z)], cmap='Greens', alpha=0.4)

            return None
        
    def validation_curve(self, error_train, error_val, lambda_vec):
        """graphically analyzes the best value of the lambda hyperparameter for normalization"""

        plt.figure(figsize = (10, 5))
        plt.plot(lambda_vec, error_train, '-o', lambda_vec, error_val, '-o', lw = 2)
        plt.legend(['Train', 'Cross Validation'])
        plt.xlabel('lambda')
        plt.ylabel('Error')

        return 
    
    def learning_rate_lr_neural_net(self, X, y, Xtest, ytest, num_iterations = 1500, learning_rates = [0.01, 0.001, 0.0001]):
        '''analyzing different learning rates'''
        
        lr = LrNeuralNetwork(self.X, self.y)
        models = {}
        for i in learning_rates:
            print ("learning rate is: " + str(i))
            models[str(i)] = lr.model(X, y, Xtest, ytest, num_iterations, learning_rate = i, interval = 50, print_cost = False)
            print ('\n' + "-------------------------------------------------------" + '\n')
        for i in learning_rates:
            plt.plot(np.squeeze(models[str(i)]["costs"]), label= str(models[str(i)]["learning_rate"]))
        plt.ylabel('cost')
        plt.xlabel('iterations (hundreds)')
        legend = plt.legend(loc='upper center', shadow=True)
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        plt.show()

        return None
    
    def learning_curve(self, error_train, erro_val):
        """learning curve for bias vs variance analysis"""

        m = self.y.size 
        plt.figure(figsize = (10, 5))
        plt.plot(np.arange(1, m+1), error_train, np.arange(1, m+1), erro_val, lw=2)
        plt.title('Learning Curve')
        plt.legend(['Training', 'Cross Validation'])
        plt.xlabel('Number of trainable examples')
        plt.ylabel('Error')

        return None
    
    def learning_curve_train(self, costs, learning_rate):
        '''learning curve for training in neural networks'''

        costs = np.squeeze(costs)
        plt.plot(costs)
        plt.ylabel('cost')
        plt.xlabel('iterations (per hundreds)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        return None
    
    def predicted_values(self, Xtest, ytest, pred):
        """visualization of expected data with that obtained"""

        plt.figure(figsize = (10,5))
        plt.scatter(Xtest, ytest, label = 'correct values')
        plt.scatter( Xtest, pred, label = 'predict values')
        plt.legend()
        plt.grid(True)
        plt.box(False)
        plt.title('Predicted Values')

        return None