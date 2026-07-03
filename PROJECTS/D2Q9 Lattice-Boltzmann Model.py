#Numerical modeling and simulation----D2Q9 Lattice-Boltzmann Model. "D2" means 2 Dimensions, and "Q9" means the fluid particles can move in 9 discrete directions (up, down, left, right, the four diagonals, and stationary).
import numpy as np
import matplotlib.pyplot as plt
plot_every=50 #decrease THIS TO SPEED UP


def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2 + (y2-y1)**2)

def main():
    Nx=400  #What it is: You are setting up the universe. The grid is 400 cells wide (Nx) and 100 cells tall (Ny). The simulation will run for 3000 frames (Nt).
    Ny=100
    tau=0.53 # Why it matters: tau is the "relaxation time."#It mathematically controls the viscosity (thickness) of the fluid.
    Nt=30000  #INCREASE THIS TO SPEED UP  # A number very close to 0.5 makes the fluid act like air or water (very runny), which creates beautiful, swirling vortices.


    #lattice speed and weights.Imagine a tic-tac-toe board. cxs and cys are the X and Y coordinates mapping the 9 ways a particle can move. For example, (1, 0) means moving right. (0, 1) means moving up.
    NL=9
    cxs=np.array([0,0,1,1,1,0,-1,-1,-1])
    cys=np.array([0,1,1,0,-1,-1,-1,0,1])
    weights=np.array([4/9,1/9,1/36,1/9,1/36,1/9,1/36,1/9,1/36])#The weights are predefined fractions used in Lattice-Boltzmann math. Straight movements get a higher weight (1/9) than diagonal movements (1/36) because diagonals are physically further away. The center (0,0) gets the most weight (4/9) because a lot of fluid just stays put.

    #initial condition.Creating the Fluid and The Wind
    F=np.ones([Ny,Nx,NL])+0.01*np.random.randn(Ny,Nx,NL)#F is your fluid. It is a 3D grid. For every single pixel on your 400x100 screen, you are storing 9 numbers (how much fluid is moving in each of the 9 directions).
    F[:,:,3]=2.3#You start everything at 1, but add a tiny bit of random noise (.01 * random). That noise acts as a tiny imperfection in the air, which is exactly what triggers real-world turbulence. Setting F[:,:,3] = 2.3 forces a constant "wind" blowing to the right across the whole screen.

    cylinder=np.full([Ny,Nx],False)#Building the Obstacle (The Cylinder). You create a blank canvas of "False" (empty space). Then, you loop through every pixel. If a pixel is within a radius of 13 units from a specific center point (Nx//4, Ny//2), you label it "True" (solid wall).

    for y in range(0,Ny):#This puts a round pillar in the left side of your wind tunnel. The fluid will be forced to crash into this pillar and flow around it.
        for x in range(0,Nx):#
            if(distance(Nx//4,Ny//2,x,y)<13):
                cylinder[y][x]=True

    #MAIN LOOP
    for it in range(Nt):#This starts the clock. Everything inside this loop happens 3000 times to create 3000 frames of animation.
        print(it)

        F[:,-1,[6,7,8]]=F[:,-2,[6,7,8]]
        F[:,0,[6,7,8]] = F[:,1,[6, 7, 8]]

        for i,cx,cy in zip(range(NL),cxs,cys):#The np.roll function works like a conveyor belt. It literally shifts all the fluid data one pixel over in whatever direction that specific data layer is supposed to go.
            F[:,:,i]=np.roll(F[:,:,i],cx,axis=1)
            F[:,:,i]=np.roll(F[:,:,i],cy,axis=0)

        bndryF=F[cylinder,:]#This is how Lattice-Boltzmann handles solid objects. The fluid hits the wall and bounces perfectly backward.
        bndrF=bndryF[:,[0,5,6,7,8,1,2,3,4]]#What happens to the fluid that accidentally stepped inside the solid rock cylinder during the streaming step? We grab that trapped fluid (bndryF), and we reverse its direction. The array [0,5,6,7,8,1,2,3,4] is a mirror. It swaps "up" with "down", and "left" with "right".


        #fluid variable
        rho=np.sum(F,2)
        ux=np.sum(F*cxs,2)/rho
        uy=np.sum(F*cys,2)/rho

        F[cylinder,:]=bndrF
        ux[cylinder]=0
        uy[cylinder]=0

        # COLLISION
        Feq=np.zeros(F.shape)# Feq stands for "Equilibrium". When fluid particles crash into each other, they try to settle down into a balanced, natural state based on their density and velocity. You are setting up a loop to calculate what that balanced state should be
        for i,cx,cy,w in zip(range(NL),cxs,cys,weights):
            Feq[:,:,i]=rho*w*(
                1+3*(cx*ux+cy*uy)+9*(cx*ux+cy*uy)**2/2-3*(ux**2+uy**2)/2
            )
        F=F+ -(1/tau)*(F-Feq)

        if (it % plot_every == 0):
            plt.cla()  # Clear the axis first
            #dfydx=ux[2:,1:-1]-ux[0:-2,1:-1]###COMMENT THIS WHEN DO NOT WANT SWIRLS
            #dfxdy=uy[1:-1,2:]-uy[1:-1,0:-2]###COMMENT THIS WHEN DO NOT WANT SWIRLS
            #curl=dfydx-dfxdy###COMMENT THIS WHEN DO NOT WANT SWIRLS
            #plt.imshow(curl,cmap='bwr') ###COMMENT THIS WHEN DO NOT WANT SWIRLS
             #Calculate velocity
            vel = np.sqrt(ux ** 2 + uy ** 2) ###UNCOMMENT THIS, to get the grfreen and yellow and purple design

             #Draw the fluid and the colorbar
            im = plt.imshow(vel, cmap='viridis')###UNCOMMENT THIS
            cbar = plt.colorbar(im)###UNCOMMENT THIS

            plt.pause(0.01)
            cbar.remove()  ###UNCOMMENT THIS# Remove the colorbar before the next frame draws








if __name__ == "__main__":
    main()



















