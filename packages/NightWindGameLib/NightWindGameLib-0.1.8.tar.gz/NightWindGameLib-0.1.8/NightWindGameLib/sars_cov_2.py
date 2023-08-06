import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from sklearn.neighbors import NearestNeighbors

n = 1
n1 = 1


class point:
    def __init__(self):
        self.x = np.random.normal()
        self.y = np.random.normal()
        self.color = 'g'

    def get_loc(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def move(self):
        random = np.random.random()
        if random < 0.25:
            self.x += 0.1
        elif 0.25 <= random < 0.5:
            self.x -= 0.1
        elif 0.5 <= random < 0.75:
            self.y += 0.1
        else:
            self.y -= 0.1


l = []
for i in range(500):
    s = point()
    l.append(s)

l1=[]
for i in np.random.random(n):
    l[int(len(l)*i)].set_color('r')
    l1.append(l[int(len(l)*i)])

fig = plt.figure()

scat = plt.scatter([x.get_loc()[0] for x in l],
                   [x.get_loc()[1] for x in l],
                   c=[x.get_color() for x in l])


def animate(i):
    print(i)
    for j in l:
        j.move()

    # 传播机制，每次从距离最近的五个人中传播给一个人
    l2 = []
    for j in set(l1):
        nnarray = NearestNeighbors(n_neighbors=5).fit(np.array([x.get_loc() for x in l])).\
            kneighbors(np.array(j.get_loc()).reshape(1, -1), return_distance=False)[0]
        nn = nnarray[int(np.random.random()*len(nnarray))]
        l[nn].set_color('r')
        l2.append(l[nn])

    for j in l2:
        l1.append(j)
    scat.set_offsets([[x.get_loc()[0], x.get_loc()[1]] for x in l])
    scat.set_color([x.get_color() for x in l])
    return scat,


anim = animation.FuncAnimation(fig, animate, frames=100, interval=60, blit=False)
plt.show()
