# Train and save a JJE model



# Try to use GPU




import os
import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

# ex - 'path/to/images'
path_2_imgs = ""

save_file = "jje.pt"

num_epochs = 5

# Define the CNN architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 2)

    def forward(self, x):
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Instantiate the CNN
net = Net()

# Define a loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# Data handling

class JJEDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        # images divided into 2 subfolders of the root directory
        # folder names are no & yes - or whatever you want
        # the idea is:
        # not attractive | attractive 
        self.jje_categories = ['no', 'yes']
        self.images = []
        self.categories = []
        for category in self.jje_categories:
            dir_path = os.path.join(root_dir, category)
            for file in os.listdir(dir_path):
                if file.endswith(".jpg"):
                    file_path = os.path.join(dir_path, file)
                    self.images.append(file_path)
                    self.categories.append(int(category[1:]))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = Image.open(self.images[idx])
        category = self.categories[idx]
        if self.transform:
            image = self.transform(image)
        return image, category

# Define a transform to preprocess the data
transform = transforms.Compose([transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])

# Create the dataset and dataloader
dataset = JJEDataset(root_dir=path_2_imgs, transform=transform)
dataloader = DataLoader(dataset, batch_size=4,
                        shuffle=True, num_workers=4)

# Use the dataloader to train the model
for epoch in range(num_epochs):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(dataloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
    print('Epoch %d loss: %.3f' %
          (epoch + 1, running_loss / len(dataloader)))

print('Finished Training')

# Save the model
torch.save(net.state_dict(), save_file)