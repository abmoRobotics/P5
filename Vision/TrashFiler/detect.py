from model import UNET
import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
import numpy as np
import cv2
import torchvision
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2
from datetime import date, datetime


model = UNET(in_channels=3, out_channels=1)
checkpoint = torch.load("model1.pth.tar")

model.load_state_dict(checkpoint['state_dict'])
model.eval()
model.cuda()

img = Image.open("data/test_images/20160225_114531_641_1.jpg")
img1 = Image.open("data/test_images/20160225_114531_641_361.jpg")
img2 = Image.open("data/test_images/20160225_114531_641_1081.jpg")
preprocess = transforms.Compose([
    #transforms.Resize((160*2, 240*2)),
    transforms.ToTensor(),
    # transforms.Normalize(
    #     mean=[0.0,0.0, 0.0],
    #     std=[1.0,1.0,1.0]
    # )   
])

img = preprocess(img)
img1 = preprocess(img1)
img2 = preprocess(img2)
torchvision.utils.save_image(img1, "test2.png")

img = torch.unsqueeze(img, 0)
img1 = torch.unsqueeze(img1, 0)
img2 = torch.unsqueeze(img2, 0)
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print(type(img))
# print(device)
# img.to(device)
img1 = img1.cuda()
img2 = img2.cuda()
img = img.cuda()
model(img)
now = datetime.now()
p = model(img1)
print("Time: ", datetime.now()-now)
torchvision.utils.save_image(p, "test1.png")
