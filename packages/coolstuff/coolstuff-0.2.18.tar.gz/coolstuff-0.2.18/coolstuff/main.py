# Basic
import json
import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt


from models import *
from FunctionalityAnalysis import FunctionalityAnalysis
from ComprehensibilityAnalysis import ComprehensibilityAnalysis
from RobustnessAnalysis import RobustnessAnalysis
from Interface import *

# PyTorch
import torch
import torch.optim as optim
import torchvision
import torchvision.models as models
from torchvision import datasets, transforms as T
from captum.attr import GuidedGradCam, LayerGradCam, LayerAttribution, Lime, FeaturePermutation

# PyTorch adversarial-robustness
from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import PyTorchClassifier
from art.utils import load_mnist
from art.metrics import empirical_robustness

# Scikit
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from PIL import Image

# Tensorflow
import tensorflow as tf

print(tf.__version__)

def main(params):
    # pytorch_titanic()
    pytorch_cifar()
    # pytorch_imagenet()
    # scikit()
    # tensorflow_titanic()


def pytorch_titanic():  # everything is in Jupyter
    titanic_data = pd.read_csv('data/titanic.csv', index_col=0)
    # Set random seed for reproducibility.
    np.random.seed(131254)

    # Convert features and labels to numpy arrays.
    labels = titanic_data["survived"]  # .to_numpy()
    titanic_data = titanic_data.drop(['survived'], axis=1)
    data = titanic_data.to_numpy()
    feature_names = list(titanic_data.columns)

    # Separate training and test sets using
    test_indices = list(np.random.choice(len(labels), int(0.3 * len(labels)), replace=False))
    x_test = data[test_indices]
    y_test = labels[test_indices]

    # Load model
    net = TitanicSimpleNNModel()
    net.load_state_dict(torch.load('models/titanic_model.pt'))

    # Transform to correct format
    x_test = torch.as_tensor(x_test, dtype=torch.float)
    y_test = y_test.to_numpy()
    # Analysis
    interface = PyTorchInterface(net, x_test, y_test, metric_name='accuracy')
    functionality = FunctionalityAnalysis(interface)
    # functionality.plot_confusion_matrix()
    print(functionality.compute_metric())  # is in Jupyter
    comprehensibility = ComprehensibilityAnalysis(interface)  # is in Jupyter
    comprehensibility.visualize_pca(dataset=False, n_components=3, function=net.linear2)  # is in Jupyter

    # analysis.permutation_importance(feature_names, plot=True)  # is in Jupyter
    # analysis.vis_feature_importance(feature_names=feature_names, class_label=1)  # is in Jupyter
    # analysis.plot_single_attribute(num=1, feature_names=feature_names, class_label=1)  # is in Jupyter


def pytorch_cifar():  # Everything in Jupyter
    transform = T.Compose([T.ToTensor(), T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=1000,
                                             shuffle=False, num_workers=4)
    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
    x_test, y_test = next(iter(testloader))

    model = CIFAR10SimpleModel()
    PATH = 'models/cifar_net.pth'
    model.load_state_dict(torch.load(PATH))

    interface = PyTorchInterface(model, x_test, y_test, metric_name='accuracy')
    robustness = RobustnessAnalysis(interface)
    criterion = nn.CrossEntropyLoss()
    example = 9  # 9 car, 11 truck
    robustness.fast_gradient_sign_method(num_classes=10, criterion=criterion, visualize=True, eps=0.05,
                                         example=example, classes=classes)
    analysis = ComprehensibilityAnalysis(interface)
    analysis.vis_pca_tb(dataset=True)
    analysis.integrated_gradients(img_index=9)  # is in Jupyter
    analysis.grad_cam(model.conv2, img_index=example, class_labels=classes)  # Done with imagenet in Jupyter

    classifier = PyTorchClassifier(
        model=model,
        loss=criterion,
        input_shape=x_test.shape[1:],
        nb_classes=10,
    )
    x_test = x_test.detach().numpy()
    metric = empirical_robustness(classifier, x_test, attack_name='fgsm',  # In Jupyter
                                  attack_params={'max_iter': 10, 'max_eval': 10, 'init_eval': 2})
    print(metric)


def pytorch_imagenet():  # Everything is in Jupyter
    image = Image.open('data/imagenet_dogs/ILSVRC2012_val_00023440.JPEG')

    with open('data/imagenet_class_index.json') as json_file:
        class_labels = json.load(json_file)

    class_labels = [class_labels[i][1] for i in class_labels]
    alexnet = models.alexnet(pretrained=True)
    alexnet.eval()

    transform = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor(),
                           T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
    x_test = transform(image)
    x_test = x_test.unsqueeze(0)
    y_test = torch.tensor(217).unsqueeze(0)
    print(x_test.shape)
    interface = PyTorchInterface(alexnet, x_test, y_test, metric_name='accuracy')
    comprehensibility = ComprehensibilityAnalysis(interface)
    # print(alexnet.features[10])
    comprehensibility.integrated_gradients(0)  # In Jupyter
    comprehensibility.grad_cam(alexnet.features[10], 0, class_labels=class_labels)  # In Jupyter
    criterion = nn.CrossEntropyLoss()


def scikit():  # everything in Jupyter
    # Titanic dataset
    titanic_data = pd.read_csv('data/titanic.csv', index_col=0)
    labels = titanic_data["survived"]
    titanic_data = titanic_data.drop(['survived'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(titanic_data, labels, random_state=1, train_size=0.8)

    model = MLPClassifier(hidden_layer_sizes=(5, 2), random_state=3, max_iter=1000)
    # model = LogisticRegression()
    model.fit(x_train.to_numpy(), y_train.to_numpy())


    interface = SciPyInterface(model, x_test.to_numpy(), y_test.to_numpy(), metric_name='accuracy')
    analysis = ComprehensibilityAnalysis(interface)
    functionality = FunctionalityAnalysis(interface)
    print(functionality.compute_metric())
    functionality.plot_confusion_matrix()
    # analysis.visualize_pca(dataset=True, n_components=3, vis3d=True)


def tensorflow_titanic():  # everything in Jupyter
    titanic_data = pd.read_csv('data/titanic.csv', index_col=0)
    labels = titanic_data["survived"]
    titanic_data = titanic_data.drop(['survived'], axis=1)
    x_train, x_test, y_train, y_test = train_test_split(titanic_data, labels, random_state=1, train_size=0.8)
    model = tf.keras.models.Sequential([
          tf.keras.layers.Dense(128, activation='relu'),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(10)
        ])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                      loss=loss_fn,
                      metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=2)
    x_test = tf.convert_to_tensor(x_test)
    interface = TensorFlowInterface(model, x_test, y_test.to_numpy(), metric_name='accuracy')
    functionality = FunctionalityAnalysis(interface)
    print(f'accuracy: {functionality.compute_metric()}')
    functionality.plot_confusion_matrix()
    # PCA visualization
    comprehensibility = ComprehensibilityAnalysis(interface)
    comprehensibility.visualize_pca(dataset=False, n_components=3, function=model.layers[2])
    # This visualizes the PCA's of the embedding after the second linear layer.


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='analysis of model')

    parser.add_argument('--checkpoint', type=str, default=None, help='specify checkpoint of model')

    args = parser.parse_args()
    main(args)

