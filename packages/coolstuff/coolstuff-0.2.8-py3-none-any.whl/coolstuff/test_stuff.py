import numpy as np
from eli5.permutation_importance import get_score_importances
from models import CNN
from task import *
from dataloader import *

checkpoint = 'models/version_23/checkpoints/epoch=49.ckpt'
imgs_dir = 'models/h5py_num_imgs_10000_batch_size_1000'
model = CNN(n_actions=4)
task = ImitationLearning.load_from_checkpoint(checkpoint, max_epochs=10, model=model)
datamodule = ImageActionDataModule(imgs_dir, 1000, perc_val=0)
datamodule.setup()
trainloader = datamodule.train_dataloader()
x_test, y_test, indices = next(iter(trainloader))

y_pred = task.model(x_test)
y_pred = y_pred.argmax(dim=1)