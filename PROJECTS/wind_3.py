#TASK 1

import numpy as np          # Numerical arrays and math functions
import matplotlib.pyplot as plt  # Plotting library

def task1():
    # Frequency ratio r
    r = np.linspace(0.0, 3.0, 1000)
    r = r[r != 1.0]

    # Damping factors (same as before)
    zeta_values = [0.0, 0.10, 0.15, 0.20, 0.40, 1.0]

    def Q_of_r_zeta(r, zeta):
        den = np.sqrt((1.0 - r ** 2) ** 2 + (2.0 * zeta * r) ** 2)
        return np.where(den == 0, np.nan, 1.0 / den)

    # Plot
    plt.figure(figsize=(6, 4))
    for zeta in zeta_values:
        Q = Q_of_r_zeta(r, zeta)
        plt.plot(r, Q, label=f"ζ = {zeta:.2f}")

    plt.xlabel("Frequency ratio r = f / fn")
    plt.ylabel("Dynamic response ratio Q = X / X0")
    plt.title("Frequency response of SDOF system with damping")
    plt.xlim(0.0, 3.0)
    plt.ylim(0.0, 6.0)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
task1()                            #------- #TO RUN TASK 1 USE REMOVE HASH   ---------

#-------------
#TASK 2
#-------------
def tower_properties(L):
    # Return (k, m_eff, f_n) for a steel tower of length L (m).
    rho_steel = 7800.0
    E_steel   = 210e9
    D_outer   = 3.4
    t_wall    = 0.03

    m_nacelle = 67000.0
    m_rotor   = 37000.0

    D_inner = D_outer - 2.0 * t_wall
    A_tower = 0.25 * np.pi * (D_outer**2 - D_inner**2)
    I_tower = (np.pi / 64.0) * (D_outer**4 - D_inner**4)

    m_tower = rho_steel * A_tower * L
    m_eff   = m_nacelle + m_rotor + 0.5 * m_tower

    k = 3.0 * E_steel * I_tower / (L**3)

    omega_n = np.sqrt(k / m_eff)
    f_n     = omega_n / (2.0 * np.pi)

    return k, m_eff, f_n
### THIS IS TASK 2A
def task2a():

    rho = 7800.0;
    E = 210e9;
    L = 62.0;
    D_outer = 3.4;
    t = 0.03
    m_nacelle = 67000.0;
    m_rotor = 37000.0;
    zeta = 0.15;
    F0 = 1.0e4;
    rpm = 9.0

    D_inner = D_outer - 2 * t
    A = 0.25 * np.pi * (D_outer ** 2 - D_inner ** 2)
    I = (np.pi / 64.0) * (D_outer ** 4 - D_inner ** 4)

    m_tower = rho * A * L
    m_eff = m_nacelle + m_rotor + 0.5 * m_tower
    k = 3 * E * I / L ** 3
    f_n = (1 / (2 * np.pi)) * np.sqrt(k / m_eff)

    f_3P = 3 * rpm / 60.0
    r = f_3P / f_n
    Q = 1 / np.sqrt((1 - r ** 2) ** 2 + (2 * zeta * r) ** 2)
    u0 = Q * (F0 / k)

    print(" Dynamic Response Ratio (Q) =", Q)
    print(" Displacement Amplitude (u0) =", u0, "m")
task2a()

### THIS IS TASK 2B
def task2b():
    k, m_eff, f_n = tower_properties(62.0)  # tower natural frequency for 62 m tower

    rpm_1P_res = 60 * f_n  # 1P resonance speed in rpm
    rpm_3P_res = 20 * f_n  # 3P resonance speed in rpm

    rpm = np.linspace(0.0, rpm_1P_res, 300)  # plot from 0 up to 1P resonance speed
    f_1P = rpm / 60.0  # 1P line
    f_3P = rpm / 20.0  # 3P line = 3*rpm/60

    plt.figure(figsize=(8, 5))  # create figure
    plt.plot(rpm, f_1P, label='1P')  # plot 1P line
    plt.plot(rpm, f_3P, label='3P')  # plot 3P line
    plt.axhline(f_n, color='r', linestyle='--', label=f'Tower natural frequency = {f_n:.3f} Hz')  # fn line

    plt.axvline(9, color='black', linestyle=':')  # left operating-speed limit
    plt.axvline(19, color='black', linestyle=':')  # right operating-speed limit

    plt.plot(rpm_3P_res, f_n, 'o')  # mark 3P resonance point
    plt.plot(rpm_1P_res, f_n, 'o')  # mark 1P resonance point

    plt.text(rpm_3P_res + 0.3, f_n + 0.02, f'3P resonance\n{rpm_3P_res:.2f} rpm')  # label 3P resonance
    plt.text(rpm_1P_res - 4.0, f_n + 0.02, f'1P resonance\n{rpm_1P_res:.2f} rpm')  # label 1P resonance

    plt.text(13.2, 1.95 * f_n, 'Operating range\n9-19 rpm')  # simple range label

    plt.xlim(0, rpm_1P_res + 0.5)  # x-axis from 0 to just beyond 1P resonance
    plt.ylim(0, 1.1)  # y-axis from 0
    plt.xlabel('Rotor speed [rpm]')  # x-axis label
    plt.ylabel('Frequency [Hz]')  # y-axis label
    plt.title('Campbell Diagram - 62 m Tower')  # plot title
    plt.grid(True)  # grid
    plt.legend()  # legend
    plt.tight_layout()  # tidy layout
    plt.show()  # show figure

    print(f"Natural frequency = {f_n:.3f} Hz")
    print(f"1P resonance speed = {rpm_1P_res:.2f} rpm")
    print(f"3P resonance speed = {rpm_3P_res:.2f} rpm")
task2b()

#-------
#TASK 3
#-------
def task3():
    k, m_eff, f_n = tower_properties(84.0)     # call the same function, but now for 84 m tower

    rpm_1P_res = 60 * f_n                      # 1P resonance speed in rpm
    rpm_3P_res = 20 * f_n                      # 3P resonance speed in rpm

    rpm = np.linspace(0.0, 19.0, 300)          # plot from 0 to max operating speed
    f_1P = rpm / 60.0                          # 1P frequency line
    f_3P = rpm / 20.0                          # 3P frequency line

    plt.figure(figsize=(8,5))                  # create the figure
    plt.plot(rpm, f_1P, label='1P')            # draw 1P line
    plt.plot(rpm, f_3P, label='3P')            # draw 3P line
    plt.axhline(f_n, color='r', linestyle='--', label=f'Tower natural frequency = {f_n:.3f} Hz')  # natural frequency line

    plt.axvline(9, color='gray', linestyle=':', linewidth=2)
    plt.axvline(19, color='gray', linestyle=':', linewidth=2)
    plt.text(11.0, 0.55, 'Operating range\n9-19 rpm')  # label operating range

    if rpm_3P_res <= 19:
        plt.plot(rpm_3P_res, f_n, 'o')         # mark 3P resonance if inside plot range
        plt.text(rpm_3P_res + 0.3, f_n + 0.02, f'3P resonance\n{rpm_3P_res:.2f} rpm')

    if rpm_1P_res <= 19:
        plt.plot(rpm_1P_res, f_n, 'o')         # mark 1P resonance if inside plot range
        plt.text(rpm_1P_res + 0.3, f_n + 0.02, f'1P resonance\n{rpm_1P_res:.2f} rpm')

    plt.xlim(0, 22)                         # x-axis limit
    plt.ylim(0, 1.0)                           # y-axis limit
    plt.xlabel('Rotor speed [rpm]')            # x-axis label
    plt.ylabel('Frequency [Hz]')               # y-axis label
    plt.title('Campbell Diagram - 84 m Tower') # plot title
    plt.grid(True)                             # add grid
    plt.legend()                               # show legend
    plt.tight_layout()                         # improve spacing
    plt.show()                                 # display the plot

    print(f"Natural frequency = {f_n:.3f} Hz")
    print(f"1P resonance speed = {rpm_1P_res:.2f} rpm")
    print(f"3P resonance speed = {rpm_3P_res:.2f} rpm")

task3()