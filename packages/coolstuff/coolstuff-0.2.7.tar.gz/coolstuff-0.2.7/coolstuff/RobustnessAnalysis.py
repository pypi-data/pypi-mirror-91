import numpy as np
from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import PyTorchClassifier
import matplotlib.pyplot as plt


class RobustnessAnalysis:

    def __init__(self, interface):
        self.interface = interface
        self.model = interface.model
        self.x_test = interface.x_test
        self.y_test = interface.y_test
        self.y_pred = interface.y_pred
        self.metric = interface.metric

    def fast_gradient_sign_method(self, num_classes, criterion, num_channels=3, visualize=False, eps=0.3,
                                  example=0, classes=None):
        """
        Only works for PyTorch
        :param classes:
        :param example:
        :param visualize:
        :param num_classes:
        :param criterion:
        :param eps:
        :return:
        """
        classifier = PyTorchClassifier(
            model=self.model,
            loss=criterion,
            input_shape=self.x_test.shape[1:],
            nb_classes=num_classes,
        )
        x_test = self.interface.to_numpy(self.x_test)
        predictions = classifier.predict(x_test)
        y_pred = np.argmax(predictions, axis=1)
        print(f'accuracy without attack: {self.interface.accuracy(self.y_test, y_pred)}')

        # Attack
        attack = FastGradientMethod(estimator=classifier, eps=eps)
        x_test_adv = attack.generate(x=self.x_test)
        predictions = classifier.predict(x_test_adv)
        y_pred_att = np.argmax(predictions, axis=1)
        print(f'accuracy with attack: {self.interface.accuracy(self.y_test, y_pred_att)}')

        if classes is None:
            classes = range(num_classes)

        if visualize:
            fig, axs = plt.subplots(1, 3)
            axs[0].set_axis_off()
            axs[0].set_title(f'Original image\npredicted: {classes[self.y_pred[example]]}')
            axs[1].set_axis_off()
            axs[1].set_title('Added noise')
            axs[2].set_axis_off()
            axs[2].set_title(f'Distorted image\npredicted: {classes[y_pred_att[example]]}')
            fig.suptitle(f'Original label: {classes[self.y_test[example]]}')

            print(self.x_test.shape)
            image = self.interface.to_numpy(self.x_test)
            image = image.transpose(0, 2, 3, 1)
            image_adv = self.interface.to_numpy(x_test_adv)
            image_adv = image_adv.transpose(0, 2, 3, 1)
            axs[0].imshow(image[example, :, :, :num_channels])
            axs[1].imshow(np.asarray(image_adv[example, :, :, :num_channels]) -
                          np.asarray(image[example, :, :, :num_channels]))
            axs[2].imshow(image_adv[example, :, :, :num_channels])
            plt.show()