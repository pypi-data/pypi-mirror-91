from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np


class FunctionalityAnalysis:

    def __init__(self, interface):
        self.interface = interface
        self.model = interface.model
        self.x_test = interface.x_test
        self.y_test = interface.y_test
        self.y_pred = interface.y_pred

    def plot_confusion_matrix(self, num_datapoints=1000):
        cm = confusion_matrix(y_pred=self.y_pred[:num_datapoints], y_true=self.y_test[:num_datapoints], normalize='true')
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()
        plt.show()

    def     compute_metric(self):
        return self.interface.metric(self.y_test, self.y_pred)
