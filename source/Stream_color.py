import cv2
import numpy as np
import matplotlib.pyplot as plt


fname="/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/Pf01.bin"
limit=3225.42578
file = open(fname, "rb")
# >f collects data in bigIndian float format
print("collecting data ..!")
data = np.fromfile(file, dtype='>f')

u = open("/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/Uf01.bin", "rb")
v = open("/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/Vf01.bin", "rb")
dataU = np.fromfile(u, dtype='>f')
dataV = np.fromfile(v, dtype='>f')

grid = np.zeros((500,500,100), dtype=np.float32)
gridU = np.zeros((500,500,100), dtype=np.float32)
gridV = np.zeros((500,500,100), dtype=np.float32)

# to arrange the data to grid
for x in range(500):
    for y in range(500):
        for z in range(100):
            grid[x, y, z] = data[x + (y * 500) + (z * 250000)]
            gridU[x, y, z] = dataU[x + (y * 500) + (z * 250000)]
            gridV[x, y, z] = dataV[x + (y * 500) + (z * 250000)]


image = np.zeros((500, 500, 3), dtype=np.uint8)
i=grid[:,:,0]
maxl = np.amax(i)
minl = maxw = limit
minw = np.amin(i)
for h in range(500):
    for w in range(500):
        if (i[h, w] > limit):
            image[h, w][0] = 255
            image[h, w][1] = image[h, w][2] = 255 - int(255 * (i[h, w] - minl) / (maxl - minl))
        else:
            image[h, w][0] = image[h, w][1] = int(255 * (i[h, w] - minw) / (maxw - minw))
            image[h, w][2] = 255


fig, ax = plt.subplots()
plt.imshow(image)
x, y = np.meshgrid(np.array(range(500)), np.array(range(500)))
ax.streamplot(x,y,gridU[:,:,0][::-1], gridV[:,:,0][::-1], color=gridU[:,:,0][::-1] , cmap=plt.cm.ocean)
plt.show()

