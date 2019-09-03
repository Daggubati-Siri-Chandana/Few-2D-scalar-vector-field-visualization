import cv2
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
print("collecting data ..!")
data = np.fromfile(file, dtype='>f')

u = open("/Data/Uf01.bin", "rb")
v = open("/Data/Vf01.bin", "rb")
dataU = np.fromfile(u, dtype='>f')
dataV = np.fromfile(v, dtype='>f')
grid = np.zeros((250,250,100), dtype=np.float32)
gridU = np.zeros((250,250,100), dtype=np.float32)
gridV = np.zeros((250,250,100), dtype=np.float32)

# to arrange the data to grid
for x in range(250):
    for y in range(250):
        for z in range(100):
            if(x%2==0 or y%2==0):
                grid[x//2, y//2, z] = data[x + (y * 500) + (z * 250000)]
                gridU[x//2, y//2, z] = dataU[x + (y * 500) + (z * 250000)]
                gridV[x//2, y//2, z] = dataV[x + (y * 500) + (z * 250000)]


aggr_mat = []
aggr_matU = []
aggr_matV = []
n = int(input("\nenter the rate of aggregation along z (factor of 100): "))
for i in range(0, 100, n):
    dup = np.zeros((250,250), dtype=np.float32)
    dupU = np.zeros((250,250), dtype=np.float32)
    dupV = np.zeros((250,250), dtype=np.float32)
    for j in range(n):
        dup = np.add(dup, grid[:, :, j])
        dupU = np.add(dupU, gridU[:, :, j])
        dupV = np.add(dupV, gridV[:, :, j])
    dup /= n
    dupU /= n
    dupV /= n
    aggr_mat += [dup]
    aggr_matU += [dupU]
    aggr_matV += [dupV]
print("\ngenerating quiver plot..!")
for h in range(250):
    for w in range(250):
        if(h%2==0 or w%2==0):
            aggr_mat[0][h,w]=0
            aggr_matU[0][h,w]=0
            aggr_matV[0][h,w]=0

x=200
y=150
fig, ax = plt.subplots()
ax.quiver(aggr_mat[0][:x,:y], aggr_matU[0][:x,:y], aggr_matV[0][:x,:y],cmap=plt.cm.PiYG)
#plt.quiver(aggr_mat[0], aggr_matU[0], aggr_matV[0],width=0.02, headwidth=25,headlength=4)#,color="blue",units='xy')
plt.show()

