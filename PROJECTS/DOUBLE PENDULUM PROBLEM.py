##DOUBLE PENDULUM PROBLEM

#IMPORTING ESSENTIAL LIBRARIES
import numpy as np
from scipy.integrate import odeint #USED TO SOLVE DIFFERENTIAL EQUATION
import sympy as sm
import matplotlib.pyplot as plt

##DEFINING SYMBOLS AND VARIABLES USING SYMPY.SYMBOLS
t=sm.symbols('t')
m_1, m_2, g=sm.symbols('m_1 m_2 g', positive=True)
the1, the2=sm.symbols(r'\theta_1, \theta_2', cls=sm.Function)

the1=the1(t)
the2=the2(t)

x1=sm.sin(the1)
y1 =-sm.cos(the1)

x2=x1+sm.sin(the2)
y2=y1 -sm.cos(the2)

##CAlculating first and second derivatives of theta and energies v_xi and v_yi
the1_d=sm.diff(the1,t)#angular velocity
the1_dd=sm.diff(the1_d,t) #angular acceleration

x1_d=sm.diff(x1,t)
y1_d=sm.diff(y1,t)

the2_d=sm.diff(the2,t)#angular velocity
the2_dd=sm.diff(the2_d,t) #angular accelaeraation

x2_d=sm.diff(x2,t)
y2_d=sm.diff(y2,t)

##DEFINING KINETIC 'T' AND POTENTIAL ENERGIES 'V' AND THE LANGRANGIAN 'L' FOR THE DOUBLE PENDULUM
t_1=0.5*m_1*((x1_d)**2+(y1_d)**2) #KINETIC ENERGY OF THE FIRST MASS
t_2=0.5*m_2*((x2_d)**2+(y2_d)**2) #KINETIC ENERGY OF THE SECOND MASS

v_1=m_1*g*y1
v_2=m_2*g*y2

l=t_1+t_2-(v_2+v_1)

#WE FORMULATE LNGRANGES EQUATION FOR NON DAMPED SYSTEM SINCE WE HAVE 2 MASSES WE NEED 2 EQUATIONS
le1=sm.diff(sm.diff(l,the1_d),t )-sm.diff(l,the1)
le2=sm.diff(sm.diff(l,the2_d), t)-sm.diff(l,the2)

le1=le1.simplify()
le2=le2.simplify()

#we create a function that solves langranges equation numerically for the double pendulum system
solutions=sm.solve([le1,le2],the1_dd,the2_dd)
lef1=sm.lambdify((the1,the2,the1_d,the2_d,t,m_1,m_2,g),solutions[the1_dd])
lef2=sm.lambdify((the1,the2,the1_d,the2_d,t,m_1,m_2,g),solutions[the2_dd])

#initial conditions and constants
initial_conditions=[1,0,1,0] #angle_1, velocity_1, angle_2, velocity_2
m1_val=4  ## OVER HERE WE CAN CHANGE THE MASSES AND GRAVITY (MARS) AND GET DIFFERENT ANIMATIONS
m2_val=4   ## IN LINE 58 YOU CAN CHANGE THE VELOCITY AS WELL TO GIVE IT ANOTHER STYLE OF ANIMATION
g_val=9.81

#function representing the system of first-order ODEs
def systemofodes(y,t,m_1,m_2,g):
    the1, the1_d,the2,the2_d=y

    the1_dd=lef1(the1,the2,the1_d,the2_d,t,m_1,m_2,g)
    the2_dd=lef2(the1,the2,the1_d,the2_d,t,m_1,m_2,g)

    return[the1_d,the1_dd,the2_d,the2_dd]
#time points for numerical solution
timepoints=np.linspace(0,40,1001)

#solve the system of ODEs
solution=odeint(systemofodes,initial_conditions,timepoints,args=(m1_val,m2_val,g_val))

#extract position and velocity from the solutions
the1_sol=solution[:,0]
the1_d_sol=solution[:,1]

the2_sol=solution[:,2]
the2_d_sol=solution[:,3]

x1_pendulum=np.sin(the1_sol)
y1_pendulum=-np.cos(the1_sol)

x2_pendulum=x1_pendulum + np.sin(the2_sol)
y2_pendulum=y1_pendulum+ -np.cos(the2_sol)

###animating the solutions
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
fig,ax=plt.subplots()
ax.set_xlim(-2.5,2.5)
ax.set_ylim(-2.5,1)
plt.grid()

def update(frame):

    pendulum1.set_data([0, x1_pendulum[frame]], [0, y1_pendulum[frame]])
    mass1.set_data([x1_pendulum[frame]],[y1_pendulum[frame]])
    pendulum2.set_data([x1_pendulum[frame], x2_pendulum[frame]], [y1_pendulum[frame], y2_pendulum[frame]])
    mass2.set_data([x2_pendulum[frame]],[y2_pendulum[frame]])
    return pendulum1, mass1, pendulum2, mass2


pendulum1, = ax.plot([0, x1_pendulum[0]], [0, y1_pendulum[0]], lw=3)
mass1, = ax.plot([x1_pendulum[0]],[y1_pendulum[0]], 'o', markersize=4*int(m1_val)+1,color='red')
pendulum2, = ax.plot([x1_pendulum[0], x2_pendulum[0]], [y1_pendulum[0], y2_pendulum[0]], lw=3)
mass2, = ax.plot([x2_pendulum[0]],[y2_pendulum[0]], 'o', markersize=4*int(m2_val)+1,color='black')

animation = FuncAnimation(fig, update, frames=len(timepoints) , interval=25, blit=True)

plt.show()