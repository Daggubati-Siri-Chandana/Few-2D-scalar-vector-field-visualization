import numpy as np
import matplotlib.pyplot as plt


class IndexTracker(object):
    def __init__(self,fig,ax,U,V):
        self.fig = fig
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')
        self.U = U
        self.V = V
        rows, cols, self.slices = U.shape
        self.ind = 0
        x, y = np.meshgrid(np.array(range(500)), np.array(range(500)))
        self.x=x
        self.y=y
        self.im=ax.streamplot(self.x, self.y, self.U[:,:,self.ind][::-1], self.V[:,:,self.ind][::-1], color=self.U[:,:,self.ind][::-1] , cmap=plt.cm.ocean)
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.ax.clear()
        self.im=ax.streamplot(self.x, self.y, self.U[:,:,self.ind][::-1], self.V[:,:,self.ind][::-1], color=self.U[:,:,self.ind][::-1] , cmap=plt.cm.ocean)
        ax.set_ylabel('slice %s' % self.ind)
        self.fig.canvas.draw()

u = open("/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/A2_Data/Uf06.bin", "rb")
v = open("/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/Data/A2_Data/Vf06.bin", "rb")

print("collecting data ..!")
dataU = np.fromfile(u, dtype='>f')
dataV = np.fromfile(v, dtype='>f')

gridU = np.zeros((500,500,100), dtype=np.float32)
gridV = np.zeros((500,500,100), dtype=np.float32)

# to arrange the data to grid
for x in range(500):
    for y in range(500):
        for z in range(100):
            gridU[x, y, z] = dataU[x + (y * 500) + (z * 250000)]
            gridV[x, y, z] = dataV[x + (y * 500) + (z * 250000)]

print("\ncollected data of dimensions 500*500*100")
print(".........................................................")

fig, ax = plt.subplots(1, 1)
tracker = IndexTracker(fig,ax,gridU,gridV)

fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()
