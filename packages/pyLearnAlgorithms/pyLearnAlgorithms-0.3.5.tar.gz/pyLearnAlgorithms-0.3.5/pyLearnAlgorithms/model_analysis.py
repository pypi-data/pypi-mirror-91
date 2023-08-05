import numpy as np

class ModelAnalysis():

    def __init__(self, correct_values, predict_values):
        '''initializing the correct data and the predicted data'''

        self.correct_values = correct_values
        self.predict_values = predict_values

        return None

    def accuracy(self):
        '''for binary problems, calculates the percentage of correct answers'''

        accuracy = np.mean(self.predict_values == self.correct_values) * 100

        return accuracy

    def confusion_matrix(self):
        '''confusion matrix for algorithm analysis'''

        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0
        for index in range(0, len(self.predict_values)):
            if self.correct_values[index] == 1 and self.predict_values[index] == 1:
                true_positive += 1
            elif self.correct_values[index] == 0 and self.predict_values[index] == 1:
                false_positive += 1
            elif self.correct_values[index] == 0 and self.predict_values[index] == 0:
                true_negative += 1
            elif self.correct_values[index] == 1 and self.predict_values[index] == 0:
                false_negative += 1
        
        matrix = [[true_positive, false_positive], [false_negative, true_negative]]

        return matrix
    
    def precision(self):
        '''analysis of the fraction of predicted data that actually belongs to the predicted class'''

        matrix = self.confusion_matrix()
        if (matrix[0][0] + matrix[0][1]) != 0:
            precision = matrix[0][0] / (matrix[0][0] + matrix[0][1])
        else:
            precision = 0

        return precision
    
    def recall(self):
        '''analysis of the fraction of predicted data that was actually classified correctly'''

        matrix = self.confusion_matrix()
        if (matrix[0][0] + matrix[1][0]) != 0:
            recall = matrix[0][0] / (matrix[0][0] + matrix[1][0])
        else:
            recall = 0

        return recall

    def average(self):
        '''trading off precision and recall'''

        precision = self.precision()
        recall = self.recall()
        average = (precision + recall) / 2

        return average

    def f_score(self):
        '''trading off precision and recall'''

        precision = self.precision()
        recall = self.recall()
        if (precision + recall) != 0:
            f_score = 2 * ((precision * recall) / (precision + recall))
        else:
            f_score = 0

        return f_score


