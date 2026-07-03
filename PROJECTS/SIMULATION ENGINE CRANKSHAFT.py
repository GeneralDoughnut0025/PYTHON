#### SIMULATION ENGINE CRANKSHAFT ()SELF() ----

# RPM changes graph height a lot.
# Crank radius changes stroke and graph height.
# Rod length changes graph shape.
# Same settings = same graph every cycle.
# Velocity is slope of position.
# Acceleration is slope of velocity.

# Velocity shows how fast the piston is moving up or down.
# Acceleration shows how quickly the piston speed is changing.
# When velocity peaks, acceleration becomes zero.
# When piston changes direction, velocity becomes zero.
# A finite rod makes the curves uneven, not perfect sine waves.
# If RPM, crank radius, and rod length stay fixed, the pattern repeats every revolution.
# Higher RPM makes velocity and acceleration larger.
# Bigger crank radius increases stroke and usually increases graph size.
# Different rod length changes the shape of the curves.

# --- STEP 1: LIBRARIES AND PARAMETERS ---
import numpy as np  # math library for sin, cos, pi, sqrt.
import matplotlib.pyplot as plt  # plotting library for graphs and animation.
from matplotlib.animation import FuncAnimation  # animation tool.
from matplotlib.widgets import Slider  # slider widgets for live inputs.

rpm = 1500.0  # engine speed in revolutions per minute; higher rpm = faster motion.
crank_radius = 40.0  # crank radius in mm.# distance from crank center to crank pin; controls stroke.
rod_length = 110.0  # connecting rod length in mm.affects piston path and rod ratio.
bore = 70.0  # cylinder bore diameter in mm.used to calculate engine capacity (cc).

# --- STEP 2: THE MATH (KINEMATICS) ---
def calculate_positions(angle_degrees, crank_r, rod_l, rpm_value):  # function to compute engine motion values.
    theta = np.radians(angle_degrees)  # convert angle from degrees to radians.

    crank_x = crank_r * np.cos(theta)  # x-position of crank pin.horizontal position of crank pin.
    crank_y = crank_r * np.sin(theta)  # y-position of crank pin.vertical position of crank pin.

    piston_x = 0.0  # piston stays on the centerline, so x is always zero.
    piston_y = crank_y + np.sqrt(rod_l**2 - crank_x**2)  # piston y-position from crank-slider geometry.# piston height from crank-slider geometry.

    rad_sec = rpm_value * (2 * np.pi / 60)  # convert RPM to radians per second.
    ratio = crank_r / rod_l  # rod-to-crank ratio used in velocity/acceleration formulas.

    velocity = -crank_r * rad_sec * (np.sin(theta) + (ratio * np.sin(2 * theta)) / 2)  # piston velocity in mm/s.
    acceleration = -crank_r * (rad_sec**2) * (np.cos(theta) + ratio * np.cos(2 * theta))  # piston acceleration in mm/s^2.

    return crank_x, crank_y, piston_x, piston_y, velocity, acceleration  # send all values back.

# --- STEP 3: SETTING UP THE DRAWING ---
fig, (ax_engine, ax_graph) = plt.subplots(1, 2, figsize=(13, 7))  # create 2 side-by-side plots.
plt.subplots_adjust(bottom=0.32, wspace=0.30)  # leave enough room for sliders below.

cx, cy, px, py, vel, accel = calculate_positions(45, crank_radius, rod_length, rpm)# Test the math by calculating positions at 45 degrees. takes values from line 26,27&28

crank_line, = ax_engine.plot([0, cx], [0, cy], 'bo-', linewidth=4, label="Crank")  # draw crank line. cx=horizontal position of the crank end and cy=vertical position of the crank end
#ax_engine.plot([0, cx], [0, cy])---- draws a line between the origin and the crank tip.So cx and cy are just the destination point of that line
rod_line, = ax_engine.plot([cx, px], [cy, py], 'ro-', linewidth=4, label="Connecting Rod")  # draw rod line.
piston_marker, = ax_engine.plot([px], [py], 'gs', markersize=25, label="Piston")  # draw piston marker.
# ([cx, px], [cy, py])-----draws a line between two points, point 1 = (cx, cy) and point 2 = (px, py) it needs two x-values and two y-values because it is connecting two locations.
#   WHILE This draws one point only at (px, py).So this is just a marker, not a line between two points. [px] means one x-value & [py] means one y-value

ax_engine.set_xlim(-200, 200)  # set x-axis range for engine plot.
ax_engine.set_ylim(-80, 500)  # set y-axis range for engine plot.
ax_engine.set_aspect('equal')  # keep geometry shape correct.This is important because your crank and rod have real lengths and angles. If the aspect is not equal, the mechanism may still be calculated correctly, but it can look wrong on screen.
ax_engine.grid(True)  # show grid.
ax_engine.legend(markerscale=0.6, loc="upper right")  # show legend with smaller marker size.

# --- STEP 5A: ADDING TEXT DISPLAYS ---
# Add text to the screen to show live data.
# (0.05, 0.95) are coordinates for the top-left corner of the window.
# transform=ax.transAxes means use window percentages (0 to 1) instead of engine coordinates.
data_text = ax_engine.text(0.01, 0.98, '', transform=ax_engine.transAxes, fontsize=12, verticalalignment='top') # ' ' ---makes a place for text but leave it blank for now.
#0.01 and 0.98 do give the position, but they need a rulebook for what those numbers mean. transform=ax_engine.transAxes is that rulebook.
#verticalalignment='top'-----top means you hang the sign so its top edge is fixed to the nail and make the text grow downward from that point.

# -- Setup Velocity Graph (Right) --
# We create an empty line that we will fill with data points as the engine runs
vel_line, = ax_graph.plot([], [], 'g-', linewidth=2, label="Velocity")  # green line for velocity.[] and [] mean there are no x-values or y-values yet
# [] []----you hang an empty string on the graph first,then later you slowly add dots to make the line.Because the program is probably going to add values later, one step at a time, during animation.
#Acceleration is often much bigger than velocity, so dividing by 100 makes the red line fit better on the same graph. It is just a scaling trick so both lines can be seen together.
accel_line, = ax_graph.plot([], [], 'r-', linewidth=2, label="Acceleration / 100")  # red line for scaled acceleration.

ax_graph.set_xlim(0, 360)  # x-axis covers one crank revolution.
ax_graph.set_ylim(-15000, 15000)  # starting y-axis range.
ax_graph.set_xlabel("Crank Angle (Degrees)")  # x-axis title.
ax_graph.set_ylabel("Speed / Accel")  # y-axis title.
ax_graph.set_title("Real-Time Kinematics")  # graph title.
ax_graph.grid(True)  # show graph grid.
ax_graph.legend()  # show graph legend.


# --- STEP 5B: ADDING INTERACTIVE SLIDERS ---

ax_rpm = plt.axes([0.18, 0.16, 0.70, 0.025])  # position of RPM slider.ax_rpm = plt.axes([...]) creates the small box where the slider lives.
slider_rpm = Slider(ax_rpm, 'RPM', 500.0, 5000.0, valinit=rpm)  # create RPM slider.Slider(...) puts the actual slider inside that box.
#The four numbers are the box position and size.valinit=rpm means the slider starts at the current RPM value.
ax_rod = plt.axes([0.18, 0.10, 0.70, 0.025])  # position of rod-length slider.
slider_rod = Slider(ax_rod, 'Rod Length', 80.0, 200.0, valinit=rod_length)  # create rod-length slider.

ax_crank = plt.axes([0.18, 0.04, 0.70, 0.025])  # position of crank-radius slider.
slider_crank = Slider(ax_crank, 'Crank Radius', 20.0, 80.0, valinit=crank_radius)  # create crank-radius slider.

# --- STEP 4: ANIMATION ---
##Think of them like three empty buckets:: one bucket for angles,one bucket for velocity & one bucket for acceleration
# At the start, all three buckets are empty.
angles_history = []  # store angle values for graph.
velocity_history = []  # store velocity values for graph.
accel_history = []  # store acceleration values for graph.

# 'frame' is the current angle (0, 5, 10...) passed automatically by the animation loop.
def update(frame):  # update function runs once for every animation frame.
    current_rpm = slider_rpm.val  # read current RPM from slider.
    current_rod = slider_rod.val  # read current rod length from slider.
    current_crank = slider_crank.val  # read current crank radius from slider.

    max_engine_height = current_crank + current_rod  # highest piston point possible.This calculates the highest place the piston could reach.
    ax_engine.set_ylim(-current_crank - 20, max_engine_height + 50)  # auto-resize engine y-axis.This changes the vertical viewing window of the engine picture so the whole mechanism stays visible. so nothing gets cut off.

    cx, cy, px, py, vel, accel = calculate_positions(frame, current_crank, current_rod, current_rpm)  # compute current kinematics.
    ###Using frame means the angle is taken from the current step of the animation, so it changes every time the picture updates.Easy way to think about it.
    # .45 = one photo.frame = a whole photo album, one page at a time.
    ##The animation has to keep updating the drawing. So each time the picture changes, this line recalculates the newest positions and motion values from the current slider settings and current frame.

    #These lines mean: take the parts you already drew, and move them to their new positions.
    crank_line.set_data([0, cx], [0, cy])  # move crank line.Think of 'crank_line' as the crank stick you already drew.So 'set_data' is the part that says where the line should go now.
    rod_line.set_data([cx, px], [cy, py])  # move rod line.
    piston_marker.set_data([px], [py])  # move piston marker.

    ##FORMULAS in code
    stroke = 2 * current_crank  # stroke is twice the crank radius.full piston travel from top to bottom.
    rod_ratio = current_rod / stroke  # rod ratio = rod length / stroke. rod length divided by stroke; important engine geometry ratio.
    displacement = max_engine_height - py  # piston distance down from top dead center.
    mean_piston_speed_mps = (2 * (stroke / 1000) * current_rpm) / 60  # mean piston speed in m/s. depends on stroke and rpm
    engine_cc = ((np.pi / 4) * (bore**2) * stroke) / 1000  # single-cylinder displacement in cc.engine swept volume in cubic centimeters (cc)

    data_text.set_text(  # update the text shown on the engine plot.
        f"Angle: {frame % 360:03d}°\n"  # show crank angle.
        f"RPM: {current_rpm:.0f}\n"  # show rpm.
        f"Stroke: {stroke:.1f} mm\n"  # show stroke.
        f"Rod Ratio: {rod_ratio:.2f}\n"  # show rod ratio.
        f"Pos from Top: {displacement:.1f} mm\n"  # show piston displacement.
        f"Mean Piston Speed: {mean_piston_speed_mps:.2f} m/s\n"  # show mean piston speed.
        f"Engine Capacity: {engine_cc:.1f} cc"  # show engine displacement.
    )

    ###this block is part of the animation update work
    
    if frame == 0:  # if animation restarts from 0 degrees.It means: when the animation loops back to the start, delete the old saved graph values so the new animation begins cleanly.
        angles_history.clear()  # clear old angle data.
        velocity_history.clear()  # clear old velocity data.
        accel_history.clear()  # clear old acceleration data.

    #These three lines are saving the new values so the graph can draw a line over time instead of just showing one number.
    #Because the graph needs to remember the old values and the new values together.If you only kept the latest number, you would never get a line graph.You would only have one dot.
    angles_history.append(frame)  # add new angle to history.
    velocity_history.append(vel)  # add new velocity to history.
    accel_history.append(accel / 100)  # add scaled acceleration to history.

    vel_line.set_data(angles_history, velocity_history)  # update velocity graph line.use all the saved angle values and velocity values to redraw the green line,
    accel_line.set_data(angles_history, accel_history)  # update acceleration graph line.use all the saved angle values and acceleration values to redraw the red line.

    max_val = max(max(np.abs(velocity_history)), max(np.abs(accel_history)), 1) * 1.2  # find safe graph limit.finds the biggest value from:: the velocity history,the acceleration history&1 as a minimum backup(1 is just a backup value so the graph never gets a zero-size range)
    #max_val means: the biggest height the graph should show right now.So max_val decides how tall the graph window should be.
    ax_graph.set_ylim(-max_val, max_val)  # auto-resize graph y-axis.This makes the graph grow or shrink based on the current data.

    return crank_line, rod_line, piston_marker, data_text, vel_line, accel_line  # return updated artists.


# FuncAnimation runs our 'update' loop.
# np.arange(0, 360, 5) generates frames 0, 5, 10... up to 355.
# interval=20 pauses for 20 milliseconds between frames. blit=False redraws everything safely.
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 5), interval=20, blit=False)  # run animation over one revolution.
plt.show()  # open the window and start the simulation.



###add one short title in your resume/project description like: “Single-cylinder crank-slider kinematics simulator with real-time piston motion, velocity, acceleration, rod ratio, and swept volume.”
##Relation ::::: If the velocity curve is rising, acceleration is positive. If the velocity curve is falling, acceleration is negative. When velocity reaches a peak or valley, acceleration passes through zero because the green curve stops rising and starts falling there.
# At top dead center and bottom dead center, piston velocity becomes zero, but acceleration is usually large because the piston is reversing direction very quickly.

##### Does it repeat? :::::: Yes — if RPM, crank radius, and rod length stay constant, the motion is periodic, so the same pattern repeats every full revolution in your current model.
#### Since your graph is plotted against crank angle from 0 to 360 degrees, one full cycle should repeat again from 360 to 720 degrees with the same shape.

#### WHICH PARAMETERS CHANGES THE GRAPHS :::: RPM: changes the size of both velocity and acceleration curves; higher RPM makes both much larger, and acceleration grows especially fast because it depends on angular speed squared. ###### Crank radius: changes stroke, so it changes piston travel and also changes velocity and acceleration magnitudes.
# ###### Rod length: changes the asymmetry and distortion of the curves, because rod ratio changes how non-sinusoidal the piston motion is. ### Rod ratio: this is really the combined effect of rod length and stroke, and it strongly affects curve shap


##For the Bullet 350 BS4, idle RPM is the speed the engine tries to maintain when the bike is standing still and the throttle is closed,
# peak torque RPM is where the engine pulls hardest, peak power RPM is where it makes maximum horsepower, and redline is the safe upper limit the engine should not continuously exceed.





