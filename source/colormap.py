import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [-1, 0, 1]
        return np.ma.masked_array(np.interp(value, x, y))

print("Enter a char to choose variable from dataset below : ")
print("\nc - Cloud moisture mixing ratio\np - Pressure\nt - Temperature")
choice = input(">>> ").lower().rstrip()
if choice=="c":
    fname="/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/QCLOUDf24.bin"
    limit=0.00332
elif choice=="p":
    fname="/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/Pf01.bin"
    limit=3225.42578
elif choice=="t":
    fname="/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/TCf24.bin"
    limit=31.51576
else:
    print("Invalid choice, please choose again\n")


file = open(fname, "rb")
# >f collects data in bigIndian float format
print("collecting data ..!")
data = np.fromfile(file, dtype='>f')
grid = np.zeros((500, 500, 100), dtype=np.float32)

# to arrange the data to grid
for x in range(500):
    for y in range(500):
        for z in range(100):
            grid[x, y, z] = data[x + (y * 500) + (z * 250000)]

print("\ncollected data of dimensions 500*500*100")
print(".........................................................")
# to get list of aggregated matrices of size 500*500 based on n value
aggr_mat = []
n = int(input("\nenter the rate of aggregation along z (factor of 100): "))
for i in range(0, 100, n):
    # performing an aggregation of 20 cells in z direction
    dup = np.zeros((500, 500), dtype=np.float32)
    for j in range(n):
        dup = np.add(dup, grid[:, :, j])
    dup /= n
    aggr_mat += [dup]

print("\ngenerating color map..!")
image = np.zeros((500, 500, 3), dtype=np.uint8)
for i in aggr_mat:
    # i is having a two d matrix of 500*500
    maxl = np.amax(i)
    minl = maxw = limit
    minw = np.amin(i)
    for h in range(500):
        for w in range(500):

            #two color map
            #image[h, w][0] = 0
            #image[h, w][1] = int(255 * (i[h, w] - minw) / (maxl - minw))
            #image[h, w][2] = 255 - int(255 * (i[h, w] - minw) / (maxl - minw))
            
            #diverging
            if (i[h, w] > limit):
                image[h, w][0] = 255
                image[h, w][1] = image[h, w][2] = 255 - int(255 * (i[h, w] - minl) / (maxl - minl))
            else:
                image[h, w][0] = image[h, w][1] = int(255 * (i[h, w] - minw) / (maxw - minw))
                image[h, w][2] = 255
            
    fig = plt.figure()
    norm = MidpointNormalize(vmin=minw, vmax=maxl,midpoint = minl)
    ax = fig.add_subplot(111)
    imgplot = plt.imshow(image)
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap=plt.cm.seismic))
    plt.show()
'''
fig = plt.figure()
ax = fig.add_subplot(111)
cax=ax.matshow(aggr_mat[0], cmap=plt.cm.rainbow)
fig.colorbar(cax)
plt.show()
'''
