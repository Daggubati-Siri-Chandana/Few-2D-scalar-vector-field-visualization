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

grid = np.zeros((125,125,100), dtype=np.float32)
gridU = np.zeros((125,125,100), dtype=np.float32)
gridV = np.zeros((125,125,100), dtype=np.float32)

# to arrange the data to grid
for x in range(500):
    for y in range(500):
        for z in range(100):
            if(x%4==0 or y%4==0):
                grid[x//4, y//4, z] = data[x + (y * 500) + (z * 250000)]
                gridU[x//4, y//4, z] = dataU[x + (y * 500) + (z * 250000)]
                gridV[x//4, y//4, z] = dataV[x + (y * 500) + (z * 250000)]

aggr_mat = []
aggr_matU = []
aggr_matV = []
n = int(input("\nenter the rate of aggregation along z (factor of 100): "))
for i in range(0, 100, n):
    dup = np.zeros((125,125), dtype=np.float32)
    dupU = np.zeros((125,125), dtype=np.float32)
    dupV = np.zeros((125,125), dtype=np.float32)
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

max=np.amax(aggr_mat)
maxU=np.amax(aggr_matU)
maxV=np.amax(aggr_matV)

min=np.amin(aggr_mat)
minU=np.amin(aggr_matU)
minV=np.amin(aggr_matV)
for h in range(125):
    for w in range(125):
        if(aggr_mat[0][h,w]>limit):
            aggr_mat[0][h,w] = (aggr_mat[0][h,w] - limit) / (max - limit)
        else:
            aggr_mat[0][h,w] = (aggr_mat[0][h,w] - min) / (limit - min)

        if(aggr_matU[0][h,w]>85.17703):
            aggr_matU[0][h,w] = (aggr_matU[0][h,w] - 85.17703) / (maxU - 85.17703)
        else:
            aggr_matU[0][h,w] = (aggr_matU[0][h,w] - minU) / (85.17703 - minU)

        if(aggr_matV[0][h,w]>82.95293):
            aggr_matV[0][h,w] = (aggr_mat[0][h,w] - 82.95293) / (maxV - 82.95293)
        else:
            aggr_matV[0][h,w] = (aggr_mat[0][h,w] - minV) / (82.95293 - minV)


x=aggr_mat[0][::-1]
y=aggr_matU[0][::-1]
z=aggr_matV[0][::-1]

p, q = np.meshgrid(np.array(range(125)), np.array(range(125)))
fig, ax = plt.subplots()
ax.streamplot(p,q, y[:,:], z[:,:], color = x[:,:] , cmap=plt.cm.ocean)
ax.quiver(x[:,:] , y[:,:], z[:,:], cmap=plt.cm.PiYG)

plt.show()

