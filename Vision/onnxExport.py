from torch.autograd import Variable
from model.model import UNET
import torch.onnx
import torchvision
import torch

dummy_input = Variable(torch.randn(1, 3, 256, 256)).to("cuda")
#state_dict = torch.load('model/crack500BrightnessAugmentationv5.pth.tar')
model = UNET(in_channels=3, out_channels=1)
checkpoint = torch.load("model/crack500BrightnessAugmentationv5.pth.tar")
model.load_state_dict(checkpoint['state_dict'])
model.eval()
model.cuda()
    #model.load_state_dict(state_dict)
torch.onnx.export(model, dummy_input, "moment-in-time.onnx")