import torch
import pytorch_lightning as pl
import torch.nn.functional as F


class ImitationLearning(pl.LightningModule):
    """
    Imitation learning task that loads batches in h5 format and learns to predict a discrete action (0, 1, 2, 3)
    given an observation (image of 4 by 84 by 84). It also saves hyperparameters and logs the accuracy and loss to
    Tensorboard. It can be used for both training and validation.
    """
    def __init__(self, model, lr, batch_size, max_epochs, tot_ep_trained=0, weight_decay=0, pretrained=False,
                 alpha=1, perc_val=0, dropout=0):
        super().__init__()
        self.model = model
        self.train_accuracy = pl.metrics.Accuracy()
        self.val_accuracy = pl.metrics.Accuracy()
        self.lr = lr
        self.weight_decay = weight_decay
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.alpha = alpha
        self.end = 38  # magic number 38 which indicates where the blocks begin/end
        self.train_max_acc = 0
        self.val_max_acc = 0
        tot_ep_trained = int(tot_ep_trained + self.max_epochs)  # Assuming the model trains to the end
        self.save_hyperparameters({'model': model.__class__.__name__,
                                   'lr': lr,
                                   'batch_size': batch_size,
                                   'tot_ep_trained': tot_ep_trained,
                                   'weight_decay': weight_decay,
                                   'pretrained': pretrained,
                                   'alpha': alpha,
                                   'perc_val': perc_val,
                                   'dropout': dropout})

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr, weight_decay=self.weight_decay)

    def shared_forward_pass(self, images, actions):
        if self.alpha != 1:  # Only execute when alpha not equal to 1 to keep speed when
            images[:, :, :self.end, :] = images[:, :, :self.end, :] * self.alpha
        pred_actions = self.model(images)
        loss = F.cross_entropy(pred_actions, actions)
        return loss, pred_actions

    def training_step(self, batch, batch_idx):
        images, actions, indices = batch
        loss, pred_actions = self.shared_forward_pass(images, actions)

        # Logging every log_every_n_steps
        self.log('train/train_loss', loss)
        self.log('train/train_acc', self.train_accuracy(pred_actions, actions), prog_bar=True)

        return {'loss': loss}

    def training_epoch_end(self, outputs):
        # log accuracy for whole epoch
        train_epoch_acc = self.train_accuracy.compute()
        self.log('train/train_acc_epoch', train_epoch_acc)

        # Track the maximum train accuracy
        if train_epoch_acc > self.train_max_acc:
            self.train_max_acc = train_epoch_acc

    def validation_step(self, val_batch, batch_idx):
        images, actions, indices = val_batch
        loss, pred_actions = self.shared_forward_pass(images, actions)
        acc = self.val_accuracy(pred_actions, actions)
        return {'val_loss': loss, 'val_accuracy': acc}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        avg_acc = self.val_accuracy.compute()
        self.log("val/val_accuracy_epoch", avg_acc, prog_bar=True)
        self.log("val/val_loss_epoch", avg_loss, prog_bar=True)

        # Track the maximum val accuracy
        if avg_acc > self.val_max_acc:
            self.val_max_acc = avg_acc

    def on_epoch_end(self):
        # Every epoch log both the max training and validation accuracy
        self.logger.log_hyperparams(params=dict(self.hparams),
                                    metrics={'train/max_accuracy': self.train_max_acc,
                                             'val/max_accuracy': self.val_max_acc})