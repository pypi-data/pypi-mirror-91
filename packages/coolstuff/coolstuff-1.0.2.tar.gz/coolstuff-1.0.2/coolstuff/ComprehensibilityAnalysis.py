from torch.utils.tensorboard import SummaryWriter
from sklearn.decomposition import PCA
import plotly.express as px
import tensorflow as tf
import tensorboard as tb
import warnings
import numpy as np
import matplotlib.pyplot as plt
import torch
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile
from captum.attr import IntegratedGradients, FeaturePermutation
from captum.attr import visualization as viz
from captum.attr import LayerGradCam, LayerAttribution


class ComprehensibilityAnalysis:
    """
    Implements methods for the comprehensibility pillar
    """
    def __init__(self, interface):
        self.interface = interface
        self.model = interface.model
        self.x_test = interface.x_test
        self.y_test = interface.y_test
        self.y_pred = interface.y_pred
        self.metric = interface.metric

    def get_features(self, layer, dataset, num_datapoints):
        """
        Helper function to get features in right format and do some checks
        :param layer: the embedding of the features after this layer is taken
        :param dataset: boolean if dataset is used or not
        :param num_datapoints: number of datapoints to visualize
        :return: features in shape (n_samples, n_features) to use for PCA
        """
        if dataset:
            features = self.x_test[:num_datapoints]
        else:
            if layer is None:
                raise TypeError("Please specify function if not using dataset")
            features = self.interface.embedding_layer_output(layer, num_datapoints)
            if features is None:
                raise TypeError("embedding layer output is None, please implement it if you want to use PCA")
        features = self.interface.to_numpy(features)
        if len(features.shape) != 2:  # Bring in correct format
            features = np.reshape(features, (features.shape[0], -1))
        return features

    def visualize_pca(self, n_components, layer=None, dataset=False, num_datapoints=1000, vis3d=False):
        """
        Use PCA to visualize the dataset or the embedding after a specified layer
        :param n_components: number of components to visualize, if vis3d=True then always use 3
        :param layer: the embedding of the features after this layer is taken
        :param dataset: specify if want to visualize dataset or layer embedding
        :param num_datapoints: number of datapoints used for the visualization
        :param vis3d: specify if you want to use 3D visualizations
        :return: nothing, it shows the figure immediately
        """
        # Define features
        features = self.get_features(layer, dataset, num_datapoints)

        # PCA
        if vis3d:
            pca = PCA(n_components=3)
        else:
            pca = PCA(n_components=n_components)
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

    def vis_pca_tb(self, layer=None, num_datapoints=1000, dataset=False, vis_imgs_tb=True, num_channels=None):
        """
        Only PyTorch
        Using Tensorboard (tb) to visualize dataset or embedding. This allows for 3D visualization with
        attached images to each datapoint. This can be opened using tensorboard --logdir=vis
        Expected input if you want to use img_labels: (n_samples, n_channels, height, width)
        :param layer: the embedding of the features after this layer is taken
        :param num_datapoints: number of datapoints used for the visualization
        :param dataset: specify if want to visualize dataset or layer embedding
        :param vis_imgs_tb: visualize datapoints as images in tensorboard
        :param num_channels: number of channels to visualize, only two options 1 for grayscale and 3 for RGB
        if your image has another number of channels, this parameter has to be specified.
        :return: nothing, it outputs data in the vis folder which is used for visualization in tensorboard
        """

        # Define features
        features = self.get_features(layer, dataset, num_datapoints)

        # PCA
        pca = PCA(n_components=3)
        print(features.shape)
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
        Calculates and visualizes the permutation importance, it does this by permuting each column and calculate
        the effect on the accuracy for this shuffling. More information can be found here:
        https://christophm.github.io/interpretable-ml-book/feature-importance.html
        :param feature_names: names of the features, used for plotting
        :param plot: specify if you want to plot or only get the values
        :param title: title of the plot
        :param axis_title: axis title of the plot
        :return: nothing, it prints and plot the feature importances
        """

        def score(inputs):
            y_pred = self.model(inputs)
            return y_pred

        y_test = self.interface.from_numpy(self.y_test, dtype=torch.int64)
        feature_perm = FeaturePermutation(score)
        attr = feature_perm.attribute(inputs=self.x_test, target=y_test)
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

    def vis_feature_importance(self, feature_names, class_label=0, plot=True, title='Average Feature Importances',
                               axis_title='Features'):
        """
        Only works for PyTorch.
        Only works for classification
        This is mostly taken from the https://captum.ai/tutorials/Titanic_Basic_Interpret tutorial
        :param feature_names: names of the features, used for plotting
        :param class_label: specify for which class label you want to calculate this
        :param plot: specify if you want to plot or only get the values
        :param title: title of the plot
        :param axis_title: axis title of the plot
        :return: nothing, it prints and plot the feature importances
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

    def integrated_gradients(self, img_index):
        """
        Only works for PyTorch
        Calculates integrated gradients: https://arxiv.org/pdf/1703.01365.pdf
        :param img_index: the index of the image of the dataset (dataset assumes a batch of images)
        :return: nothing, it visualizes the integrated gradients
        """
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

    def grad_cam(self, layer, img_index, class_labels):
        """
        Only works for PyTorch and CNNs
        For more information: https://captum.ai/api/layer.html#gradcam and
        https://arxiv.org/pdf/1610.02391.pdf
        :param layer: the embedding of the features after this layer is taken
        :param img_index: the index of the image of the dataset (dataset assumes a batch of images)
        :param class_labels: class labels used for visualization
        :return: nothing, it shows a plot
        """
        y_test = self.interface.from_numpy(self.y_test, dtype=torch.int64)
        x_test = self.x_test.requires_grad_()
        gradcam = LayerGradCam(self.model, layer)
        attr = gradcam.attribute(x_test, y_test[img_index], relu_attributions=True)
        upsampled_attr = LayerAttribution.interpolate(attr, self.x_test.shape[-2:], interpolate_mode='bilinear')
        upsampled_attr = upsampled_attr.detach().numpy()
        masked_data = np.ma.masked_where(upsampled_attr < 0.001, upsampled_attr)
        org_image = x_test.detach().numpy().transpose(0, 2, 3, 1)
        plt.imshow(org_image[img_index, ...])
        plt.imshow(masked_data[img_index, 0, :, :], cmap='rainbow', alpha=0.5)
        plt.title('Gradient overlayed with image')

        output = self.model(x_test)
        output_top_5 = torch.argsort(output[0], descending=True)[:5]
        output_top_5 = [i.item() for i in output_top_5]
        plt.xlabel(f"Top 5 classes:\n"
                   f"{class_labels[output_top_5[0]]}\n"
                   f"{class_labels[output_top_5[1]]}\n"
                   f"{class_labels[output_top_5[2]]}\n"
                   f"{class_labels[output_top_5[3]]}\n"
                   f"{class_labels[output_top_5[4]]}\n")
        plt.show()
