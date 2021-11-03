
import cv2
from PIL import Image
import numpy as np
from skimage.morphology import medial_axis, skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert
import time
from fil_finder import FilFinder2D
from astropy.io import fits


# Billede vi loader for at teste
img = Image.open(r"C:\P5\P5\Vision\data\train_masks\20160328_151013_361_1281.png").convert('L') 
img = np.array(img)
(thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)

def closing(img):
    kernel = np.ones((5,5),np.uint8)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return closing

def skeletonization(img):
    skeleton = skeletonize(img)
    return skeleton

def find_length_of_skeletonization(img):
    #mask = img.data > 1
    fil = FilFinder2D(img)
    return fil
# Function for calculating the avergage width of a crack
def crack_width(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # create an empty black image
    drawing = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    # draw contours and hull points
    for i in range(len(contours)):
        print(cv2.contourArea(contours[i]))
        
        color_contours = (255,255,255) # green - color for contours
        # draw ith contour
        cv2.drawContours(drawing, contours, i, color_contours, 1, 8, hierarchy)

    return contours

contours = closing(blackAndWhiteImage)
#print(contours[0])

#img = find_length_of_skeletonization(img)
# while 1:
#     # plt.imshow(img.image.value, origin='lower')
#     # plt.title("Image")
#     plt.plot(img)
#     plt.show()
#     cv2.waitKey(30)


s1 = skeletonize(contours)
#draing = crack_width(img)

fig, axes = plt.subplots(1,2, figsize=(8, 8), sharex=True, sharey=True)
ax = axes.ravel()



ax[0].imshow(img, cmap=plt.cm.gray)
ax[0].set_title('original')
ax[0].axis('off')

ax[1].imshow(s1, cmap=plt.cm.gray)
ax[1].set_title('skeleton')
ax[1].axis('off')

fig.tight_layout()
plt.show()

# while 1:
#     cv2.imshow("Window",s1)
#     cv2.waitKey(30)