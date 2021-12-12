
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
from utils.utils import load_model
from utils.features import closing, skeletonize
from skimage.morphology import binary_closing 

detect_transform = A.Compose(
        [
            A.Resize(height=960, width=540),
            A.Normalize(
                mean=[0.0, 0.0, 0.0],
                std=[1.0, 1.0, 1.0],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )



def test_img():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    from PIL import Image
    import numpy as np
    img = Image.open(r"C:\Users\anton\Aalborg Universitet\P5 - General\1. P5 - Projektmappe\2. Programming\Vision\pavement crack datasets\CRACK500\testdata\20160308_072824.jpg")
    img = np.array(img)
    img = np.rot90(img)
    #print(img.shape)
    augmentented = detect_transform(image=img)
    data = augmentented["image"].to(device=DEVICE)
    model = load_model("model/crack500v2.pth.tar")
    data = torch.unsqueeze(data,0)
    output = torch.sigmoid(model(data))
    output = torch.squeeze(output)
    preds = (output > 0.5).float()
    a = preds.cpu().numpy()
    cv2.imwrite('output.jpg', (a*255).astype(np.uint8))
    after_closing = binary_closing(a, selem=np.ones((9, 9)))
    cv2.imwrite('closing.jpg', (after_closing*255).astype(np.uint8))
    # preds = closing(preds.cpu().numpy())
    # preds = skeletonize(preds)
    # preds = (preds*255).astype(np.uint8)


if __name__ == "__main__":
    test_img()