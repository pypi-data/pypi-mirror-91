import numpy as np
from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import PyTorchClassifier
import matplotlib.pyplot as plt


class RobustnessAnalysis:
    """
    Implements methods for the robustness pillar
    """
    def __init__(self, interface):
        self.interface = interface
        self.model = interface.model
        self.x_test = interface.x_test
        self.y_test = interface.y_test
        self.y_pred = interface.y_pred
        self.metric = interface.metric

    def fast_gradient_sign_method(self, num_classes, criterion, num_channels=3, visualize=False, eps=0.3,
                                  img_index=0, class_labels=None):
        """
        Only works for PyTorch
        Attacks a network using the fast gradient sign method: https://arxiv.org/abs/1412.6572
        :param num_classes: number of classes the network uses (e.g. 10 for CIFAR-10)
        :param criterion: loss criterion (e.g. nn.CrossEntropyLoss())
        :param num_channels: number of channels (1 for grayscale, 3 for RGB, others are also possible)
        :param visualize: specify if you want to visualize with an example image 
        :param eps: perturbation used for the adversarial attack
        :param img_index: image index from the batch of image in the dataset
        :param class_labels: class labels used for visualization
        :return: nothing, it visualizes the result and put output to screen
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
        x_test_adv = attack.generate(x=x_test)
        predictions = classifier.predict(x_test_adv)
        y_pred_att = np.argmax(predictions, axis=1)
        print(f'accuracy with attack: {self.interface.accuracy(self.y_test, y_pred_att)}')

        if class_labels is None:
            class_labels = range(num_classes)

        if visualize:
            fig, axs = plt.subplots(1, 3)
            axs[0].set_axis_off()
            axs[0].set_title(f'Original image\npredicted: {class_labels[self.y_pred[img_index]]}')
            axs[1].set_axis_off()
            axs[1].set_title('Added noise')
            axs[2].set_axis_off()
            axs[2].set_title(f'Distorted image\npredicted: {class_labels[y_pred_att[img_index]]}')
            fig.suptitle(f'Original label: {class_labels[self.y_test[img_index]]}')

            print(self.x_test.shape)
            image = self.interface.to_numpy(self.x_test)
            image = image.transpose(0, 2, 3, 1)
            image_adv = self.interface.to_numpy(x_test_adv)
            image_adv = image_adv.transpose(0, 2, 3, 1)
            axs[0].imshow(image[img_index, :, :, :num_channels])
            axs[1].imshow(np.asarray(image_adv[img_index, :, :, :num_channels]) -
                          np.asarray(image[img_index, :, :, :num_channels]))
            axs[2].imshow(image_adv[img_index, :, :, :num_channels])
            plt.show()
