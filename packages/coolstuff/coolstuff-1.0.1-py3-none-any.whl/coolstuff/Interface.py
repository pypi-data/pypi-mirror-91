from abc import ABC, abstractmethod
import tensorflow as tf
import numpy as np
import torch


class Interface(ABC):
    """
    Abstract interface used for Functionality, Comprehensibility and Robustness analysis.
    """
    def __init__(self, model, x_test, y_test, metric_name='accuracy'):
        """
        Defined 4 methods and 1 optional
        :param model: the model that is used
        :param x_test: the test set that is used
        :param y_test: the labels, expected shape after to_numpy is (n_samples)
        :param metric_name: the metric that can be used, for now either accuracy or custom but any metric can
        be implemented
        """
        metric_dict = {'accuracy': self.accuracy, 'custom': self.custom_metric}
        self.model = model
        self.x_test = x_test
        self.y_test = self.to_numpy(y_test)
        self.y_pred = self.predict(x_test)
        self.y_pred = self.to_numpy(self.y_pred)
        self.metric = metric_dict[metric_name]

        # Check if numpy array, so I know for sure which input I deal with.
        if (type(self.y_test) is not np.ndarray) or (type(self.y_pred) is not np.ndarray):
            raise ValueError('both y_test and y_pred need to be numpy arrays. Implement the'
                             ' to_numpy function correctly.')

    @abstractmethod
    def to_numpy(self, y) -> np.ndarray:
        """
        Convert your y_pred and y_test to numpy array
        This assumes that output of the model is always in the same format.
        :param y: output of model
        :return: output of model in numpy array format
        """
        pass

    @abstractmethod
    def from_numpy(self, x):
        """
        Function to reverse the to_numpy() function
        :param x: input, or output from network
        :return: the parameter in numpy format
        """
        pass

    @abstractmethod
    def predict(self, x_test):
        """
        Returns labels (y_pred) which can be used for metrics
        :param x_test: the input of the network
        :return: labels (y_pred) which can be used for metrics (e.g. accuracy or custom metric)
        """
        pass

    def embedding_layer_output(self, layer, num_datapoints):
        """
        Needed if I want to visualize the embedding of a certain output
        :param num_datapoints: number of datapoints
        :param layer: the embedding of the features after this layer is taken
        :return: the output of the layer embedding after specified layer.
        """
        pass

    def custom_metric(self, y_pred, y_test):
        pass

    # Predefined metrics
    @staticmethod
    def accuracy(y_test: np.ndarray, y_pred: np.ndarray):
        return np.mean(y_test == y_pred)


class PyTorchInterface(Interface):
    """
    PyTorch instance of Interface
    """
    def __init__(self, model, x_test, y_test, metric_name):
        super().__init__(model, x_test, y_test, metric_name)

    def to_numpy(self, y) -> np.ndarray:
        try:
            output = y.detach().numpy()
        except AttributeError:
            output = y
        return output

    def from_numpy(self, x, dtype=torch.float):
        return torch.as_tensor(x, dtype=dtype)

    def embedding_layer_output(self, layer, num_datapoints):
        activation = {}

        def get_activation(name):
            def hook(model, input, output):
                activation[name] = output.detach()
            return hook
        layer.register_forward_hook(get_activation('layer'))
        self.model(self.x_test[:num_datapoints])
        return activation['layer']

    def predict(self, x_test):
        y_pred = self.model(x_test)
        return y_pred.argmax(dim=1)


class SciPyInterface(Interface):
    """
    Scipy instance of Interface
    """
    def __init__(self, model, x_test, y_test, metric_name):
        super().__init__(model, x_test, y_test, metric_name)

    def predict(self, x_test):
        return self.model.predict(x_test)

    def to_numpy(self, y) -> np.ndarray:
        return y

    def from_numpy(self, x):
        return x

    def embedding_layer_output(self, layer, num_datapoints):
        return layer(self.x_test)


class TensorFlowInterface(Interface):
    """
    TensorFlow instance of Interface
    """
    def __init__(self, model, x_test, y_test, metric_name):
        super().__init__(model, x_test, y_test, metric_name)

    def predict(self, x_test):
        y_pred = self.model(x_test)
        return tf.math.argmax(y_pred, axis=1)

    def to_numpy(self, y) -> np.ndarray:
        return np.asarray(y)

    def from_numpy(self, x, dtype=tf.float32):
        return tf.convert_to_tensor(x, dtype=dtype)

    def embedding_layer_output(self, layer, num_datapoints):
        partial_model = tf.keras.Model(self.model.inputs, layer.output)
        return partial_model(self.x_test[:num_datapoints])

