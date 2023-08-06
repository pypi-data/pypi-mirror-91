import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    """
    Simple CNN network closely corresponding to the DQN architecture used in Breakout,
    but with added BatchNorm layers and dropout
    """
    def __init__(self, n_actions, n_channels=4, dropout=0):
        """
        Initialize the model
        :param n_actions: number of actions (labels)
        :param n_channels: number of channels
        :param dropout: specify dropout (if 0 then no dropout)
        """
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=n_channels, out_channels=32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.fc1 = nn.Linear(3136, 512)  # batch * 64 * 7 * 7 (3136)  # this parameter is image size specific
        self.fc2 = nn.Linear(512, n_actions)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)
        self.bn3 = nn.BatchNorm2d(64)
        # self.dropout = nn.Dropout(dropout)

    def forward(self, o):
        x = self.bn1(F.relu(self.conv1(o)))
        x = self.bn2(F.relu(self.conv2(x)))
        x = self.bn3(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        # x = self.dropout(x)
        x = self.fc2(x)  # use linear layer because of CrossEntropyLoss
        # x = self.dropout(x)
        return x


class TitanicSimpleNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(12, 12)
        self.sigmoid1 = nn.Sigmoid()
        self.linear2 = nn.Linear(12, 8)
        self.sigmoid2 = nn.Sigmoid()
        self.linear3 = nn.Linear(8, 2)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        lin1_out = self.linear1(x)
        sigmoid_out1 = self.sigmoid1(lin1_out)
        sigmoid_out2 = self.sigmoid2(self.linear2(sigmoid_out1))
        return self.softmax(self.linear3(sigmoid_out2))

    def predict(self, x):
        y_pred = self.model(x)
        return y_pred.argmax(dim=1)


class CIFAR10SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x