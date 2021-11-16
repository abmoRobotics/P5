import cv2
import numpy as np

from cv2 import cuda





def imageAlignerGPU(imgRef, imgOverlap):   
    MAX_FEATURES = 1000
    orb = cuda.ORB_create(MAX_FEATURES)

    img_ = imgOverlap.download()
    img_1 = imgRef.download()

    kp1, des1 = orb.detectAndComputeAsync(imgOverlap,None)

    kp2, des2 = orb.detectAndComputeAsync(imgRef,None)

    match = cuda.DescriptorMatcher_createBFMatcher(cv2.NORM_HAMMING)
    matches_gpu = match.knnMatchAsync(des1,des2,k=2)


    good = []
    matches_cpu = []
    matches_cpu = match.knnMatchConvert(matches_gpu)

    for m,n in matches_cpu:
        if m.distance < 0.03*n.distance:
            good.append(m)

  

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        
        kp1_cpu = orb.convert(kp1)
        kp2_cpu = orb.convert(kp2)

        src_pts = np.float32([ kp1_cpu[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2_cpu[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
        
        
        
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        imgOverlap_cpu = imgOverlap.download()

        imgRef_cpu = imgRef.download()

        h,w = imgOverlap_cpu.shape

        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

        dst = cv2.perspectiveTransform(pts, M)

        imgRef = cv2.polylines(imgRef_cpu,[np.int32(dst)],True,255,3, cv2.LINE_AA)

        traveled = np.int32(dst[0][0][1])

        OverlapHeight = h - traveled

        return traveled, OverlapHeight
    else:
        print("Insufficient matches")
        return -1

def imageAlignerCPU(img1, img2):


    #sift = cv2.xfeatures2d.sift_create()
    MAX_FEATURES = 100
    sift = cv2.ORB_create(MAX_FEATURES)

    # find the key points and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    match = cv2.BFMatcher()
    matches = match.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.03*n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, M)
        traveled = abs(np.int32(dst[0][0][1]))
        overlapHeight = h - traveled
        return traveled, overlapHeight
    else:
        print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))
        return 0,0

if __name__ == "__main__":
    import time
    im1 = cv2.imread("test_data/test111.png")
    im1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2 = cv2.imread("test_data/test222.png")
    im1 = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    t1 = time.time()
    for i in range (0,100):

        imageAlignerCPU(im1,im2)
    print((time.time()-t1)/100)