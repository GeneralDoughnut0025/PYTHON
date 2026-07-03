## HEAT TRANSFER ON 2D OBJECT-- PLATE HEATED AT DIFFERENT POINTS

import numpy as np
import matplotlib.pyplot as plt

# this is the rod
a=100        #this is the thermal diffusivity variable, to slow down the heat
length=100 #mm
time=4  #seconds
nodes=100

#initialization
dx=length/nodes   #having dx and dy makes in 2d
dy=length/nodes

dt=0.2*dx*dy/a
t_nodes=int(time/dt)

u=np.zeros((nodes, nodes)) +20 #plate is initilly 20 degreees celsius

#Boundary Conditions in this you can change where the heating object is loacted and give the simulation nice patterns
# example you can replace line 21 and 22 with this-->
u[0, :]=np.linspace(0,100,nodes)
u[-1, :]=np.linspace(0,100,nodes)
u[:, 0]=np.linspace(0,100,nodes)
u[:, -1]=np.linspace(0,100,nodes)
#u[0, :]=100
#[-1, :]=100

# Visualizing with plots
fig, axis=plt.subplots()
pcm=axis.pcolormesh(u, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)

#Simulating
counter=0
while counter < time:
    w=u.copy()
    for i in range(1, nodes-1):
        for j in range(1, nodes-1):
            dd_ux=(w[i-1,j]-2*w[i,j]+w[i+1,j])/dx**2
            dd_uy=(w[i,j-1]-2*w[i,j]+w[i,j+1])/dx**2
            u[i,j]=dt*a*(dd_ux+dd_uy)+w[i, j]
    counter+=dt
    print("t:{:.3f}[s], Average Temperature:{:.2f} Celsius".format(counter, np.average(u)))

    # Updating the plot

    pcm.set_array(u)
    axis.set_title("Distributiom at t:{:.3f}[s]".format(counter))
    plt.pause(0.01)


plt.show()




