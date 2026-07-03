## UNIVERSAL GAS CONSTAT SIMULATION

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')

#PV=nRT

# CONSTANTS
num_particles=1000 #n
container_size=1  #V
time_steps=1000
particle_speed=0.01 #m/s also its kinda T, more heat means more excitation so more speed

#Initial position and velocities of particles
position=np.random.rand(num_particles,2)*container_size #2 represents the x and y axis and num_particles tells it to produces random numbers ie 100 from line 7
velocities=np.random.rand(num_particles,2)*particle_speed

#CREATING OUR PLOT
fig,ax=plt.subplots()
scatter=ax.scatter(position[:,0],position[:,1], marker='o')
ax.set_xlim(0,container_size)
ax.set_ylim(0,container_size)
plt.gca().set_aspect('equal', adjustable='box')

#SIMULATION LOOP
collisions_array=[]

for step in range(time_steps):
    position+=velocities
    collisions=0
    for i in range(num_particles):
        for j in range(2):
            if position[i,j]<0 or position[i, j]>container_size:
                velocities[i,j]*=-1 #COLLISION
                collisions+=1
    collisions_array=np.append(collisions_array,collisions)
    ax.set_title(f"Collisions: {collisions} | Average: {np.mean(collisions_array):.2f}")  # instantaneous collision rate. Because your time_steps run very fast (plt.pause(0.001)), there are many frames where no particles hit a wall. When a particle finally hits a wall, the counter spikes to 1, 2, or 4 for that frame, and then immediately drops back to 0 on the next frame as the particles bounce away and travel through empty space again.

    scatter.set_offsets(position)
    plt.pause(0.001)
    if not plt.fignum_exists(fig.number):
        break

plt.show()

