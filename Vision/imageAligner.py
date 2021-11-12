import cv2
import numpy as np
import time
from cv2 import cuda





def imageAligner(imgRef, imgOverlap):   
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
