##PLOTS FOR CARNOT, OTTO, DIESEL AND VAPOR DOME (can produse steam table values +plots ie tempVSpress, entropyVSenthalpy etc)
from pylab import *
from numpy import *
import pyromat as pm #imports the PYroMat library so you can use thermodynamic property functions.
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt



###### PLOT FOR CARNOT
def plot_carnot():
  p_min=10**5
  p_max=10*10**5
  v_max=0.5
  r=4
  γ=1.4
  # Process 1-2
  p1=p_min
  v1=v_max
  v2=v1/r
  c1=p1*v1
  # Process 2-3
  c2=c1*v2**(γ-1)
  p3=p_max
  v3=(c2/p3)**(1/γ)
  # Process 3-4
  c3=p3*v3
  # Process 4-1
  c4=p1*v1**γ
  v4=(c4/c3)**(1/(γ-1))
  ####################
  # Plotting 1-2
  v=linspace(v2,v1,30)
  p=c1/v
  plot(v,p,'r-')
  # Plotting 2-3
  v=linspace(v3,v2,30)
  p=c2/v**γ
  plot(v,p,'b-')
  # Plotting 3-4
  v=linspace(v3,v4,30)
  p=c3/v
  plot(v,p,'g-')
  # Plotting 3-4
  v=linspace(v4,v1,30)
  p=c4/v**γ
  plot(v,p,'m-')
  xlabel('Volume')
  ylabel('Pressure')
  plt.title("Carnot Cycle")
  show()

####### PLOT FOR OTTO
def plot_otto():
 p_min=10**5
 p_max=20*10**5
 v_max=0.3
 r=5
 γ=1.4
 # Process 1-2
 p1=p_min
 v1=v_max
 c1=p1*v1**γ
 v2=v1/r
 p2=c1/v2**γ
 # Process 2-3
 p3=p_max
 v3=v2
 # Process 3-4
 c2=p3*v3**γ
 v4=v1
 p4=c2/v4**γ
 ####################
 #process 1-2
 v=linspace(v2,v1,50)
 p=c1/v**γ
 plot(v,p,'r-')
 #process 2-3
 v=zeros(50)+v2
 p=linspace(p2,p3)
 plot(v,p,'b-')
 #process 3-4
 v=linspace(v3,v4,50)
 p=c2/v**γ
 plot(v,p,'g-')
 #process 4-1
 v=zeros(50)+v1
 p=linspace(p1,p4)
 plot(v,p,'m-')
 text(v1,p1-1000,'1',fontsize=12)
 text(v2-0.006,p2,'2',fontsize=12)
 text(v3-0.006,p3,'3',fontsize=12)
 text(v4,p4+1000,'4',fontsize=12)
 xlabel('Volume')
 ylabel('pressure')
 plt.title("Otto Cycle")
 show()

##### PLOT FOR DIESEL
def plot_diesel():
 p_min=10**5
 #p_max=20*10**5
 v_max=0.5
 γ=1.4
 r=4
 rc=1.5
 # Process 1-2
 p1=p_min
 v1=v_max
 c1=p1*v1**γ
 v2=v1/r
 p2=c1/v2**γ
 # Process 2-3
 p3=p2
 v3=rc*v2
 # Process 3-4
 c2=p3*v3**γ
 v4=v1
 p4=c2/v4**γ
 # Plotting Part 1-2
 v=linspace(v2,v1,50)
 p=c1/v**γ
 plot(v,p,'r-')
 #2-3
 v=linspace(v2,v3,50)
 p=zeros(50)+p2
 plot(v,p,'b-')
 # 3-4
 v=linspace(v3,v4,50)
 p=c2/v**γ
 plot(v,p,'g-')
 # 4-1
 p=linspace(p1,p4,50)
 v=zeros(50)+v1
 plot(v,p,'m-')
 text(v1,p1,'1')
 text(v2,p2+4000,'2')
 text(v3,p3,'3')
 text(v4,p4,'4')
 xlabel('V')
 ylabel('P')
 plt.title("Diesel Cycle")
 show()


####PLOT FOR VAPOR DOME
def plot_dome():
 pm.config['unit_pressure'] = 'kPa' #tells PYroMat to use kilopascals for pressure input and output.
 water = pm.get('mp.H2O')#loads the multi-phase water model, which is the correct fluid for steam/water dome calculations.
 h_f = water.hs(p=10000)[0].item() # prints the saturated enthalpy values at 10000 kPa; for multi-phase water, hs() is used for saturated enthalpy states at a given pressure.
 h_g = water.hs(p=10000)[1].item()
 print(f"THERMODYNAMIC PROPERTIES OF WATER :")
 print(f"Saturated liquid enthalpy : {h_f:.4f}")
 print(f"Saturated vapor enthalpy  : {h_g:.4f}")

 T_sat = water.Ts(p=10000).item()
 T_sat_Celsius=T_sat-273.15
 print(f"Saturation temperature: {T_sat:.4f} K and in Celsius it is : {T_sat_Celsius:.4f}") # prints the saturation temperature at 10000 kPa

 s_f = water.ss(p=10000)[0].item()
 s_g = water.ss(p=10000)[1].item()
 print(f"Saturated liquid entropy : {s_f:.4f}")# which is saturated liquid
 print(f"Saturated vapor entropy  : {s_g:.4f}")# and saturated vapor values respectively

 rho_f = water.ds(p=10000)[0].item()
 rho_g = water.ds(p=10000)[1].item()
 vf = 1 / rho_f
 vg = 1 / rho_g
 print(f"Saturated liquid density: {rho_f:.4f}")
 print(f"Saturated vapor density: {rho_g:.4f}")
 print(f"Saturated liquid specific volume: {vf:.5f}")
 print(f"Saturated vapor specific volume: {vg:.5f}")
 ## WE CANNOT GET A PLOT USING JUST OPNE VALUE WE NEED AN ARRAY OF VALUES SO WE DO ....
 p=linspace(1,22000,2000)
 vf_array = 1 / water.ds(p=p)[0]
 vg_array = 1 / water.ds(p=p)[1]
 T = water.Ts(p=p)#for each pressure in the array p, give me the saturation temperature.” PYroMat returns an array of temperatures, one for each pressure value.
 print("\nARRAY OF SATURATION TEMP IN KELVIN IS:")
 print(np.round(T, 4)) #He was not trying to get just one temperature. He wanted many points so he could later draw the saturation curve for the vapor dome. A curve needs lots of points, not one.

 s = water.ss(p=p)
 s_f = s[0]  # saturated liquid entropy
 s_g = s[1]  # saturated vapor entropy
 print("\nEntropy values of saturated liquid is:")
 print(np.round(s_f, 4))
 print("Entropy values of saturated vapor is:")
 print(np.round(s_g, 4))

 h=water.hs(p=p)
 h_f = h[0]  # saturated liquid enthalpy
 h_g = h[1]  # saturated vapor enthalpy
 print("\nEnthalpy values of saturated liquid is:")
 print(np.round(h_f, 4))
 print("Enthalp values of saturated vapor is:")
 print(np.round(h_g, 4))

 den=water.ds(p=p)
 den_f = den[0]  # saturated liquid entropy
 den_g = den[1]  # saturated vapor entropy
 print("\nDensity values of saturated liquid is:")
 print(np.round(den_f, 4))
 print("Density values of saturated vapor is:")
 print(np.round(den_g, 4))


 ###NOW WE DO THE PLOTS
 fig, ax = plt.subplots(3, 2, figsize=(12, 12))
 ax[0,0].plot(s_f,T,'r-',label='Saturated liquid entropy')
 ax[0,0].plot(s_g,T,'b-',label='Saturated vapor entropy')
 ax[0,0].set_title('Temperature (K) VS Entropy')
 ax[0,0].set_xlabel('Entropy')
 ax[0,0].set_ylabel('Temperature (K)')
 ax[0,0].grid(True)
 ax[0,0].legend(loc='upper right')

 ax[0,1].plot(vf_array, p, 'm-', label='Saturated liquid specific volume')
 ax[0,1].plot(vg_array, p, 'g-', label='Saturated vapor specific volume') #withou the code on 210, Your vapor specific volume values are likely clustered near very small numbers, so if Matplotlib chooses a broad default x-range, the line can be hard to see or look compressed.
 ax[0,1].set_xlim(1.E-4,1.E-1)#zooms the x-axis into the range where your specific-volume values actually live. Without it, Matplotlib auto-scales the axis to fit the data, and because vg_array is usually very small and spans several orders of magnitude, the curve can look squashed or weird.
 ax[0,1].set_title('Specific Volume VS Density')
 ax[0,1].set_xlabel('Density')
 ax[0,1].set_ylabel('Specific Volume')
 ax[0,1].grid(True)
 ax[0,1].legend(loc='upper right')

 ax[1,0].plot(s_f,h_f, 'k-', label='Saturated liquid')
 ax[1,0].plot(s_g,h_g, 'c-',label='Saturated vapor ')
 ax[1,0].set_title('ENTROPY VS ENTHALPY')
 ax[1,0].set_xlabel('ENTROPY')
 ax[1,0].set_ylabel('ENTHALPY')
 ax[1,0].grid(True)
 ax[1,0].legend(loc='upper right')

 ax[1,1].plot(T, p, 'y-')
 ax[1,1].set_title('PRESSURE VS TEMPERATURE (VAPORIZATION CURVE)')
 ax[1,1].set_xlabel('TEMPERTURE')
 ax[1,1].set_ylabel('PRESSURE')
 ax[1,1].grid(True)

 ax[2,0].plot(h_f, p, 'b-', label='Saturated liquid enthalpy')
 ax[2,0].set_title('PRESSURE VS ENTHALPY')
 ax[2,0].set_xlabel('ENTHALPY')
 ax[2,0].set_ylabel('PRESSURE')
 ax[2,0].grid(True)
 ax[2,0].legend(loc='upper left')

 plt.tight_layout(h_pad=4)
 plt.subplots_adjust(top=0.93)
 show()#is usually the last line after all plotting commands, because it tells Matplotlib, “now draw everything.”
 # It is especially important when making multiple plots in one script.






##THIS IS WHERE THE FUNCTIONS ARE CALLED


plot_carnot()
plot_otto()
plot_diesel()
plot_dome()
