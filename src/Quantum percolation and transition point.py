import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.colors as colors
#import matplotlib.animation as animation

#環境設
n=10  #tの範囲
m=20  #xy

p=1/2
q=1-p


#ユニタリー行列
P = [[-p, q, math.sqrt(p*q), math.sqrt(p*q)],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
Q = [[0,0,0,0],[q, -p, math.sqrt(p*q), math.sqrt(p*q)],[0,0,0,0],[0,0,0,0]]
R = [[0,0,0,0],[0,0,0,0],[math.sqrt(p*q), math.sqrt(p*q), -q, p],[0,0,0,0]]
S = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[math.sqrt(p*q), math.sqrt(p*q), p, -q]]

t_list = []
x_list = []
y_list = []

phi_map = np.zeros((2*m+1, 2*m+1,4)) #np.zeros((行,列,[]の中身の数))
phi_map[m,m]= np.array([1,0,0,0])

p_map=np.zeros([2*m+1,2*m+1])

for i in range(0,2*m+1):
    p = np.dot(phi_map[i,i], np.conj(phi_map[i,i]))
    p_map[i,i]=p
    x_list.append(i)
    y_list.append(i)
print(p_map)

for t in range(0,n+1):
    t_list.append(t)
    if t == 0:
        phi_map
        p_map
    else:
        next_phi_map = np.zeros((2*m+1,2*m+1, 4))
        final_phi_map = np.zeros((2*m+1,2*m+1,4)) #誤作動起こさない為に、最終のnext_phi_mapを収納する
        for x in range(0,2*m+1):
            if x == 0:
                for y in range(m,2*m+1):
                    if y == m:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y])])
                        final_phi_map[x,y+1] = np.array([np.inner(S,next_phi_map[x,y])])
                        final_phi_map[x,y] = next_phi_map[x,y]
                    elif y == 2*m:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y]) + np.inner(S, phi_map[x,y-1])])
                        final_phi_map[x+1,y] = np.array([np.inner(Q,next_phi_map[x,y])])
                        final_phi_map[x,y] =next_phi_map[x,y]
                    else:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y])])
                        final_phi_map[x,y+1] = np.array([np.inner(S,next_phi_map[x,y])])
                        final_phi_map[x,y] =  np.array([np.inner(S, phi_map[x,y-1])+np.inner(P,phi_map[x+1,y])])
            elif x == 2*m:
                for y in range(m,2*m+1):
                    if y == m:
                        next_phi_map[x,y] = np.array([np.inner(Q, phi_map[x-1,y])])
                        final_phi_map[x,y+1] = np.array([np.inner(S,next_phi_map[x,y])])
                        final_phi_map[x,y]=next_phi_map[x,y]
                    elif y == 2*m:
                        next_phi_map[x,y] = np.array([np.inner(Q, phi_map[x-1,y]) + np.inner(S, phi_map[x,y-1])])
                        final_phi_map[x-1,y]=np.array([np.inner(P, next_phi_map[x,y])])
                        final_phi_map[x,y]=next_phi_map[x,y]
                    else:
                        next_phi_map[x,y] = np.array([np.inner(Q, phi_map[x-1,y])])
                        final_phi_map[x,y+1]=np.array([np.inner(S, next_phi_map[x,y])])
                        final_phi_map[x,y] = np.array([np.inner(S, phi_map[x,y-1])+np.inner(Q,phi_map[x-1,y])])
            else:
                for y in range(m,2*m+1):
                    if y == 0:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y]) + np.inner(Q, phi_map[x-1,y])])
                        final_phi_map[x,y+1] =np.array([np.inner(S,next_phi_map[x,y])])
                    elif y == 2*m:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y]) + np.inner(Q, phi_map[x-1,y]) + np.inner(S, phi_map[x,y-1])])
                        final_phi_map[x+1,y] = np.array([np.inner(Q,next_phi_map[x,y])])
                        final_phi_map[x-1,y] = np.array([np.inner(P,next_phi_map[x,y])])
                    else:
                        next_phi_map[x,y] = np.array([np.inner(P, phi_map[x+1,y]) + np.inner(Q, phi_map[x-1,y])])
                        final_phi_map[x,y+1] = np.array([np.inner(S,next_phi_map[x,y])])
                        final_phi_map[x,y] =np.array([np.inner(S, phi_map[x,y-1])+np.inner(P,phi_map[x+1,y])+np.inner(Q,phi_map[x-1,y])])
                    p_map[x,y] = np.dot(final_phi_map[x,y], np.conj(final_phi_map[x,y]))
        phi_map = final_phi_map

    print(t,p_map)



fig = plt.figure()
ax = Axes3D(fig)
X,Y = np.meshgrid(x_list, y_list)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("probability")

ax.set_xlim(2*m,0)
ax.set_ylim(0,2*m)
ax.set_zlim(0,0.004)

#Z軸の色を設定
offset = p_map.ravel() + np.abs(p_map.min())
fracs = offset.astype(float)/offset.max()
norm = colors.Normalize(fracs.min(), fracs.max())
clrs = cm.cool(norm(fracs))

ax.bar3d(X.ravel(), Y.ravel(), p_map.ravel() ,0.3, 0.3, -p_map.ravel(),color =clrs)#,cmap=cm.hot)
ax.w_xaxis.set_pane_color((0, 0, 0, 0))
ax.w_yaxis.set_pane_color((0, 0, 0, 0))
ax.w_zaxis.set_pane_color((0, 0, 0, 0))
plt.show()
