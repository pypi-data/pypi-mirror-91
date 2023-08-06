# Basic
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


# Tensorflow
import tensorflow as tf


def main(params):
    # pytorch_titanic()
    # pytorch_cifar()
    # pytorch_imagenet()
    # scikit()
    # tensorflow()
    tensorflow_titanic()


def pytorch_titanic():
    titanic_data = pd.read_csv('titanic.csv', index_col=0)
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
    print(functionality.compute_metric())
    # analysis = ComprehensibilityAnalysis(interface)

    #analysis.permutation_importance(feature_names, plot=True)
    # analysis.vis_feature_importance(feature_names=feature_names, class_label=1)
    # analysis.plot_single_attribute(num=1, feature_names=feature_names, class_label=1)


def pytorch_cifar():
    transform = T.Compose([T.ToTensor(), T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                           download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=1000,
                                             shuffle=False, num_workers=4)
    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    model = CIFAR10SimpleModel()
    PATH = './cifar_net.pth'
    model.load_state_dict(torch.load(PATH))
    x_test, y_test = next(iter(testloader))
    print(y_test.shape)
    interface = PyTorchInterface(model, x_test, y_test, metric_name='accuracy')
    robustness = RobustnessAnalysis(interface)
    criterion = nn.CrossEntropyLoss()
    example = 9  # 9 car, 11 truck
    print(y_test[example])
    # robustness.fast_gradient_sign_method(num_classes=10, criterion=criterion, visualize=True, eps=0.05,
    #                                      example=example, classes=classes)
    analysis = ComprehensibilityAnalysis(interface)
    # analysis.integrated_gradients(index=9)
    # analysis.grad_cam(model.conv2, example=example)
    classifier = PyTorchClassifier(
        model=model,
        loss=criterion,
        input_shape=x_test.shape[1:],
        nb_classes=10,
    )
    x_test = x_test.detach().numpy()
    metric = empirical_robustness(classifier, x_test, attack_name='hsj',
                                  attack_params={'max_iter': 10, 'max_eval': 10, 'init_eval': 2})
    print(metric)


def pytorch_imagenet():
    alexnet = models.alexnet(pretrained=True)
    # normalize = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    # transform = T.Compose([T.Resize(256), T.CenterCrop(224), T.ToTensor()])
    # dataset = datasets.ImageNet(".", split="train", transform=transform)


def scikit():
    # Titanic dataset
    titanic_data = pd.read_csv('titanic.csv', index_col=0)
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
    # analysis.vis_pca_tb(dataset=True, vis_imgs_tb=False)
    # analysis.partial_plot(feature_names=['0', '1', '2', '3'])




    # explainer = shap.KernelExplainer(model.predict_proba, X_train)
    # shap_values = explainer.shap_values(X_test)
    # shap.force_plot(explainer.expected_value[0], shap_values[0], X_test)


def tensorflow():
    num = 100
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(10)
    ])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam',
                  loss=loss_fn,
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=1)
    y_pred_raw = model(x_test[:num])
    y_pred = tf.math.argmax(y_pred_raw, axis=1)
    function = model.layers[3]

    interface = TensorFlowInterface(model, x_test[:num], y_test[:num], y_pred)
    analysis = ComprehensibilityAnalysis(interface)
    analysis.visualize_pca(function=function, n_components=4)
    analysis.vis_pca_tb(function=function, vis_imgs_tb=False)


def tensorflow_titanic():
    titanic_data = pd.read_csv('titanic.csv', index_col=0)
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
    model.fit(x_train, y_train, epochs=5)
    x_test = tf.convert_to_tensor(x_test)
    interface = TensorFlowInterface(model, x_test, y_test.to_numpy(), metric_name='accuracy')
    functionality = FunctionalityAnalysis(interface)
    print(f'accuracy: {functionality.compute_metric()}')
    functionality.plot_confusion_matrix()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='analysis of model')

    parser.add_argument('--checkpoint', type=str, default=None, help='specify checkpoint of model')

    args = parser.parse_args()
    main(args)

