from torch.utils.tensorboard import SummaryWriter
from sklearn.decomposition import PCA
import plotly.express as px
import tensorflow as tf
import tensorboard as tb
import warnings
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile
from captum.attr import IntegratedGradients, FeaturePermutation
from captum.attr import visualization as viz
from captum.attr import GuidedGradCam, LayerGradCam, LayerAttribution


class ComprehensibilityAnalysis:

    def __init__(self, interface):
        self.interface = interface
        self.model = interface.model
        self.x_test = interface.x_test
        self.y_test = interface.y_test
        self.y_pred = interface.y_pred
        self.metric = interface.metric

    def get_features(self, function, dataset, num_datapoints):
        """
        Helper function
        :param function:
        :param dataset:
        :param num_datapoints:
        :return:
        """
        if dataset:
            features = self.x_test[:num_datapoints]
        else:
            if function is None:
                raise TypeError("Please specify function if not using dataset")
            features = self.interface.embedding_layer_output(function, num_datapoints)
            if features is None:
                raise TypeError("embedding layer output is None, please implement it if you want to use PCA")
            features = self.interface.to_numpy(features)
        if len(features.shape) != 2:
            raise ValueError(f"Features not in correct format: (n_samples, n_features), but are {features.shape}")
        return features

    def visualize_pca(self, n_components, function=None, dataset=False, num_datapoints=1000, vis3d=False):
        """
        PCA taking as input (n_samples, n_features)
        :param n_components:
        :param vis3d:
        :param num_datapoints: number of datapoints
        :param dataset: boolean, using dataset or not
        :param function: if not using dataset use function.
        :param num_datapoints: number of examples to use
        :return:
        """
        # Define features
        features = self.get_features(function, dataset, num_datapoints)

        # PCA
        if vis3d:
            pca = PCA(n_components=3)
        else:
            pca = PCA(n_components=n_components)
        print(features.shape)
        components = pca.fit_transform(features)
        labels = {
            str(i): f"PC {i + 1} ({var:.1f}%)"
            for i, var in enumerate(pca.explained_variance_ratio_ * 100)}
        total_var = pca.explained_variance_ratio_.sum() * 100
        print(f'explained variance: {pca.explained_variance_ratio_}')
        print(f'reduced features shape: {components.shape}')

        # Plotting
        if vis3d:
            fig = px.scatter_3d(
                components, x=0, y=1, z=2, color=self.y_test[:num_datapoints],
                title=f'Total Explained Variance: {total_var:.2f}%',
                labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
            )
        else:
            fig = px.scatter_matrix(
                components,
                labels=labels,
                dimensions=range(n_components),
                color=self.y_test[:num_datapoints]
            )
            fig.update_traces(diagonal_visible=True)
        fig.show()

    def vis_pca_tb(self, function=None, num_datapoints=1000, dataset=False, vis_imgs_tb=True, num_channels=None):
        """
        Expected input if you want to use img_labels: (n_samples, n_channels, height, width)
        :param function:
        :param num_datapoints:
        :param dataset:
        :param vis_imgs_tb:
        :param num_channels:
        :return:
        """

        # Define features
        features = self.get_features(function, dataset, num_datapoints)

        # PCA
        pca = PCA(n_components=3)
        components = pca.fit_transform(features)
        print(f'explained variance: {pca.explained_variance_ratio_}')
        print(f'reduced features shape: {components.shape}')

        writer = SummaryWriter('vis')

        # Add correct label image
        if vis_imgs_tb:
            label_img = self.x_test[:num_datapoints]
            if len(label_img.shape) != 4:
                raise ValueError("Expected input of image to be of shape (n_samples, n_channels, height, width)")

            if label_img.shape[1] not in [1, 3]:
                warnings.warn('Expected n_channels is 1 or 3 (grayscale or RGB). Can automatically reduce by '
                              'specifying n_channels argument to 1 or 3.', UserWarning)
                if num_channels is None:
                    raise TypeError("Specify number of channels")
                else:
                    label_img = label_img[:, :num_channels, :, :]
        else:
            label_img = None
        writer.add_embedding(components,
                             metadata=self.y_test[:num_datapoints],
                             label_img=label_img)

    def permutation_importance(self, feature_names, plot=False, title='Average Feature Importances (using permutation)',
                               axis_title='Features'):
        """
        Only PyTorch
        :param feature_names:
        :param plot:
        :param title:
        :param axis_title:
        :return:
        """

        def score(inputs, target):
            y_pred = self.model(inputs)
            return y_pred

        y_test = self.interface.from_numpy(self.y_test, dtype=torch.int64)
        feature_perm = FeaturePermutation(score)
        attr = feature_perm.attribute(inputs=self.x_test, target=y_test, additional_forward_args=y_test)
        feature_importances = np.mean(attr.detach().numpy(), axis=0)

        for i in range(len(feature_names)):
            print(feature_names[i], ": ", '%.3f' % (feature_importances[i]))
        x_pos = (np.arange(len(feature_names)))

        if plot:
            plt.figure(figsize=(12, 6))
            plt.bar(x_pos, feature_importances, align='center')
            plt.xticks(x_pos, feature_names, wrap=True)
            plt.xlabel(axis_title)
            plt.title(title)
            plt.show()

    def vis_feature_importance(self, feature_names, class_label=0, title='Average Feature Importances', plot=True,
                               axis_title='Features'):
        """
        Only works for PyTorch.
        Only works for classification (maybe regression) and with not too many features as input
        This is mostly taken from the https://captum.ai/tutorials/Titanic_Basic_Interpret tutorial
        :return:
        """
        x_test = self.x_test.requires_grad_()

        ig = IntegratedGradients(self.model)
        attr, delta = ig.attribute(x_test, target=class_label, return_convergence_delta=True)
        attr = attr.detach().numpy()
        importances = np.mean(attr, axis=0)
        for i in range(len(feature_names)):
            print(feature_names[i], ": ", '%.3f' % (importances[i]))
        x_pos = (np.arange(len(feature_names)))
        if plot:
            plt.figure(figsize=(12, 6))
            plt.bar(x_pos, importances, align='center')
            plt.xticks(x_pos, feature_names, wrap=True)
            plt.xlabel(axis_title)
            plt.title(title)
            plt.show()

    def plot_single_attribute(self, num, feature_names, class_label=0):
        x_test = self.x_test.requires_grad_()
        x_test_numpy = self.x_test.detach().numpy()
        ig = IntegratedGradients(self.model)
        attr, delta = ig.attribute(x_test, target=class_label, return_convergence_delta=True)
        attr = attr.detach().numpy()
        bin_means, bin_edges, _ = stats.binned_statistic(x_test_numpy[:, num], attr[:, num], statistic='mean',
                                                         bins=6)
        bin_count, _, _ = stats.binned_statistic(x_test_numpy[:, num], attr[:, num], statistic='count', bins=6)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width / 2
        plt.scatter(bin_centers, bin_means, s=bin_count)
        plt.xlabel(f"Average {feature_names[num]} Feature Value")
        plt.ylabel("Average Attribution")
        plt.show()

    def integrated_gradients(self, img_index):
        img_flatten = self.x_test[img_index].unsqueeze(0)
        img_flatten.requires_grad = True
        ig = IntegratedGradients(self.model)
        self.model.zero_grad()
        attr_ig, delta = ig.attribute(img_flatten, target=self.y_test[img_index].item(), return_convergence_delta=True)
        attr_ig = np.transpose(attr_ig.squeeze().cpu().detach().numpy(), (1, 2, 0))
        print('Approximation delta: ', abs(delta))
        original_image = np.transpose((self.x_test[img_index].cpu().detach().numpy() / 2) + 0.5, (1, 2, 0))
        _ = viz.visualize_image_attr(attr_ig, original_image, method="blended_heat_map", sign="all",
                                     show_colorbar=True, title="Overlayed Integrated Gradients")
        org_image = self.x_test.detach().numpy().transpose(0, 2, 3, 1)
        plt.imshow(org_image[img_index, ...])
        plt.title('original image')
        plt.show()

    def grad_cam(self, layer, img_index, guided=False):
        "Grad Cam requires PyTorch and CNNs"
        y_test = self.interface.from_numpy(self.y_test, dtype=torch.int64)
        x_test = self.x_test.requires_grad_()
        if guided:
            gradcam = GuidedGradCam(self.model, layer)
            attr = gradcam.attribute(x_test, y_test[img_index])
        else:
            gradcam = LayerGradCam(self.model, self.model.conv2)
            attr = gradcam.attribute(x_test, y_test[img_index], relu_attributions=True)
        print(self.x_test.shape)
        print(self.x_test.shape[-2:])
        upsampled_attr = LayerAttribution.interpolate(attr, self.x_test.shape[-2:])
        org_image = x_test.detach().numpy().transpose(0, 2, 3, 1)
        plt.imshow(org_image[img_index, ...])
        plt.imshow(upsampled_attr.detach().numpy()[img_index, 0, :, :], cmap='hot', alpha=0.2)
        plt.show()