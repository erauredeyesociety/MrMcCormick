# Test the JJE model

import torch
import torchvision.transforms as transforms
from PIL import Image
from jje.make_model import Net

# Load the model
saved_file = "jje.pt"
net = Net()
net.load_state_dict(torch.load(saved_file))

# Define the test transform
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# judge, jury, and executioner of looking at images
def run_JJE(image_path):
    # Open the image
    img = Image.open(image_path)
    # Apply the test transform
    img_tensor = test_transform(img).float()
    # Add an extra batch dimension
    img_tensor = img_tensor.unsqueeze_(0)
    # Pass the image through the model
    output = net(img_tensor)
    # Get the index of the highest probability
    _, jje_prediction = torch.max(output.data, 1)
    # Get corresponding category
    # use whatever names you want - this is just easier for me to look at with lots of output
    categories = ['NOOOO', 'MATCH']
    choice = categories[jje_prediction.item()]
    return choice

# Test the model on an image
image_path = '1.jpg'
choice = run_JJE(image_path)
print('JJE say: ', choice)