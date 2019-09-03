import cv2
import numpy as np
import matplotlib.pyplot as plt

file = open("/Data/HGTdata.bin", "rb")
# >f collects data in bigIndian float format
datap = np.fromfile(file, dtype='>f')

image = np.zeros((500, 500, 3), dtype=np.uint8)

maxl = np.amax(datap)
minw = np.amin(datap)

for h in range(500):
    for w in range(500):
        val = datap[h + (w * 500)]
        if (val == 0.0):
            image[h, w] = [255,0,0]
        else:
            image[h, w][1] = 255
            image[h, w][2] = image[h, w][0] = 255 - int(255 * (val- minw) / (maxl - minw))



cv2.imshow("surface", image)

cv2.waitKey(0)
