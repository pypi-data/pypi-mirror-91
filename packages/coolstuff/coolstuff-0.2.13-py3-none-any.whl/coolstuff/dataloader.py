from torch.utils.data import Dataset, ConcatDataset, DataLoader, random_split, SubsetRandomSampler
import h5py
import os
import pytorch_lightning as pl
import torch


class ImageActionDataset(Dataset):
    """
    Create dataset with images as data and the corresponding actions as labels.
    Additionally it gives the index of the original image for comparison purposes.
    """

    def __init__(self, dir_imgs):
        file = h5py.File(dir_imgs, 'r')
        self.images = file['images']
        self.actions = file['actions']
        self.indices = file['indices']

    def __len__(self):
        return self.images.shape[0]

    def __getitem__(self, idx):

        images = self.images[idx]
        actions = self.actions[idx]
        indices = self.indices[idx]

        return images, actions, indices


class ImageActionDataModule(pl.LightningDataModule):
    """
    Defines the train and validation DataLoader and does some preprocessing to convert the HDF format batches
    into a single HDF dataset (which is not loaded in memory in once but can be sampled from)
    """

    def __init__(self, data_dir, batch_size, perc_val=0.05, random=True, num_workers=4):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.pin_memory = (True if torch.cuda.is_available() else False)
        self.num_workers = num_workers
        self.perc_val = perc_val
        self.random = random

    def setup(self, stage=None):
        # Concatenate all the batches in the directory
        list_data = []
        for i in range(len(os.listdir(self.data_dir))):
            filename = f'{i}.h5'
            dataset = ImageActionDataset(dir_imgs=os.sep.join([self.data_dir, filename]))
            list_data.append(dataset)
        self.concat_dataset = ConcatDataset(list_data)

        # Divide in train and test set
        length_val_set = int(len(self.concat_dataset) * self.perc_val)
        length_train_set = len(self.concat_dataset) - length_val_set

        # Get the exact same train and validation split for reproducability and consistency
        if self.random:
            self.data_train, self.data_val = random_split(self.concat_dataset, [length_train_set, length_val_set],
                                                          generator=torch.Generator().manual_seed(42))
            # print(f'length train: {len(self.data_train)}')
            # print(f'length val: {len(self.data_val)}')
        else:
            train_idxs = range(length_train_set)
            valid_idxs = range(length_train_set, len(self.concat_dataset))
            self.train_sampler = SubsetRandomSampler(train_idxs)
            self.valid_sampler = SubsetRandomSampler(valid_idxs)

    def train_dataloader(self):
        #print(f'train loader is loaded')
        if self.random:
            return DataLoader(self.data_train, batch_size=self.batch_size, shuffle=True,
                              num_workers=self.num_workers, pin_memory=False)
        else:
            return DataLoader(self.concat_dataset, batch_size=self.batch_size, shuffle=False,
                              num_workers=self.num_workers, pin_memory=False, sampler=self.train_sampler)

    def val_dataloader(self):
        if self.perc_val != 0.0:
            # print(f'val loader is loaded')
            if self.random:
                return DataLoader(self.data_val, batch_size=self.batch_size, shuffle=False,
                                  num_workers=self.num_workers, pin_memory=False)
            else:
                return DataLoader(self.concat_dataset, batch_size=self.batch_size, shuffle=False,
                                  num_workers=self.num_workers, pin_memory=False, sampler=self.valid_sampler)