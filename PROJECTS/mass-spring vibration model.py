## mass-spring vibration model

import numpy as np # Imports NumPy, a library for numerical math, arrays, and matrices.
from scipy.integrate import odeint # Imports 'odeint' from SciPy, a numerical solver for Ordinary Differential Equations (ODEs).
import sympy as sm # Imports SymPy, a library for symbolic math (solving calculus/algebra using letters instead of numbers).
import matplotlib.pyplot as plt

##DEFINING CONSTANTS AND VARIABLES
t=sm.symbols('t') # Creates a symbolic math variable 't' to represent time in our equations.In symbolic math (which SymPy handles), we want t to remain a pure, abstract letter so we can do algebra and calculus with it, just like we would on paper.If you just type t = 5 in standard Python, the program treats t as the number 5.
# (explanation for line 5 )You are telling Python: "Create a mathematical symbol named 't', and store it in the Python variable t. Do not evaluate it as a number."This allows you to write equations like 5*t + t and have Python simplify it to 6*t instead of crashing because it doesn't know what number t represents.
m,k=sm.symbols('m k', positive=True)## Creates symbolic variables for mass (m) and stiffness (k), and tells the math engine they are positive values.
q=sm.symbols('q', cls=sm.Function) #sm.function states that the position is a function.It is a function that can change over time and be differentiated.We use 'cls=sm.Function' to tell SymPy that 'q' is NOT a static constant.
q=q(t) #specifying the variable.# This explicitly tells the math engine that position 'q' depends on time 't'.

##CALCULATING DERIVATIVES
dq_dt=sm.diff(q,t)# 1. First Derivative (Velocity)# sm.diff() calculates the derivative of position 'q' with respect to time 't'. # This gives us velocity (dq/dt).
ddq_dt=sm.diff(dq_dt,t)# 2. Second Derivative (Acceleration) # We differentiate the velocity 'dq_dt' with respect to time 't' to get the second derivative of position, which is acceleration (d²q/dt²).

##DEFINING Kinetic and POTENTIAL ENERGY
T=0.5*m*dq_dt**2 # kinetic energy
V=0.5*k*q**2 # potential energy
L=T-V #this is lagerange

#FORMULATING ;ANGRANGE EQUATION
dL_d_dq=sm.diff(L, dq_dt)
L_equation=sm.diff(dL_d_dq,t)-sm.diff(L,q)
L_equation=L_equation.simplify()

lagrange_eq = sm.solve(L_equation, ddq_dt)[0]
lagrange_eq_func=sm.lambdify((q,t,m,k),lagrange_eq)

#INITIAL CONDITIONS AND CONSTANTS
initial_conditions=[1.0,0.0] #initial position and velocity
m_val=2
k_val=2

#Functions representing the systems first-order ODEs
def system_of_odes(y,t,m,k):
    q,dq_dt=y
    ddq_dt=lagrange_eq_func(q,t,m,k)
    return[dq_dt,ddq_dt]
#time points for numerical solution
time_points=np.linspace(0,10,100)

#solve the system of ODEs
solution=odeint(system_of_odes,initial_conditions,time_points,args=(m_val,k_val))

#EXTRACT POSITION AND VELOCITY FROM THE SOLUTION
positions=solution[:,0]
velocities=solution[:,1]

plt.figure()
plt.plot(time_points, positions, label='positions') # Added 'positions'
plt.plot(time_points, velocities, label='velocities') # Added 'velocities'
plt.title('Mass-Spring Vibration Response')
plt.xlabel('Time (s)')
plt.ylabel('Displacement / Velocity')
plt.legend()
plt.grid()
plt.show()

##this code is a mass-spring vibration model written in Python. It simulates how a spring-mass system moves with time, and the “solution” is the position and velocity of the mass at every time step.
#This is a simple structural dynamics model. You are telling the computer:there is a mass m and there is a spring with stiffness k
#the mass starts at some initial position and velocity,and the program calculates how it vibrates over time.So the code is not just “plotting a graph.” It is solving the motion of a physical system.
#In simple words ===== You build a virtual spring and mass. You tell it the starting position and speed. Python calculates how it bounces. The graph shows that motion. Your “solution” is not one single number. It is the full motion history of the system over time.
