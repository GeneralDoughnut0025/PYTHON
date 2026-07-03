## HEAT TRANSFER ON 1D OBJECT-- ROD

import numpy as np
import matplotlib.pyplot as plt

# this is the rod
a=100        #this is the thermal diffusivity variable, to slow down the heat
length=100 #mm
time=12  #seconds
nodes=20

#initialization
dx=length/nodes #having only dx makes it single axis
dt=0.5*dx**2/a
t_nodes=int(time/dt)

u=np.zeros(nodes) +20 #plate is initilly 20 degreees celsius

#Boundary Conditions
u[0]=100
u[-1]=100

# Visualizing with plots
fig, axis=plt.subplots()
pcm=axis.pcolormesh([u], cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
axis.set_ylim([-2,3])

#Simulating
counter=0
while counter < time:
    w=u.copy()
    for i in range(1, nodes-1):
        u[i]=dt*a*(w[i-1]-2*w[i]+w[i+1])/dx**2+w[i]
    counter+=dt
    print("t:{:.3f}[s], Average Temperature:{:.2f} Celsius".format(counter, np.average(u)))

    # Updating the plot

    pcm.set_array([u])
    axis.set_title("Distributiom at t:{:.3f}[s]".format(counter))
    plt.pause(0.01)


plt.show()