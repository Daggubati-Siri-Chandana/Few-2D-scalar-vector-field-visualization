from mpl_toolkits import mplot3d
import cv2
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

print("Enter a char to choose variable from dataset below : ")
print("\nc - Cloud moisture mixing ratio\np - Pressure\nt - Temperature")
choice = input(">>> ").lower().rstrip()
if choice=="c":
    fname="/Data/QCLOUDf24.bin"
    limit=0.00332
elif choice=="p":
    fname="/Data/Pf01.bin"
    limit=3225.42578
elif choice=="t":
    fname="/Data/TCf24.bin"
    limit=31.51576
else:
    print("Invalid choice, please choose again\n")

file = open(fname, "rb")
# >f collects data in bigIndian float format
datap = np.fromfile(file, dtype='>f')
pgrid = np.zeros((500, 500, 100), dtype=np.float32)

# to arrange the data to grid
for x in range(500):
    for y in range(500):
        for z in range(100):
            pgrid[x, y, z] = datap[x + (y * 500) + (z * 250000)]

# to get list of aggregated matrices of size 500*500 based on n value
paggr_mat = []
n = int(input("\nenter the rate of aggregation along z (factor of 100): "))
for i in range(0, 100, n):
    # performing an aggregation of 20 cells in z direction
    dup = np.zeros((500, 500), dtype=np.float32)
    for j in range(n):
        dup = np.add(dup, pgrid[:, :, j])
    dup /= n
    paggr_mat += [dup]
print("\ngenerating contour map..!")
x, y = np.meshgrid(np.array(range(500)), np.array(range(500)))

mat = np.zeros((500, 500), dtype=np.float32)

i=paggr_mat[0]
maxl = np.amax(i)
minl = maxw = limit
minw = np.amin(i)
for h in range(500):
    for w in range(500):
        if (i[h, w] > limit):
            mat[h,w]= (i[h, w] - minl) / (maxl - minl)
        else:
            mat[h, w] = ((i[h, w] - minw) / (maxw - minw))- 1
plt.contour(x,y,mat[::-1],cmap=plt.cm.seismic)
#plt.contour(x,y,mat[::-1],[0,0.5,1],cmap=plt.cm.seismic)
plt.show()
