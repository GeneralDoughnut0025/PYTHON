# This is wind assignment 1 part1 c
#first we clean the data since we are using a new data set

import pandas as pd   # Imports the pandas library and gives it the short name pd.
from statsmodels.tsa.stattools import acf
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

df = pd.read_excel("Malmoe A stripped 2.xlsx", header=None)  # Reads the Excel file into a table called df; header=None means there are no column names in the file.
df.columns = ["wind_dir_deg", "wind_speed"]   # Gives names to the two columns: first is wind direction, second is wind speed.
speed = df["wind_speed"].copy()      # Takes only the wind speed column and stores it in a new variable called speed.

speed = pd.to_numeric(speed, errors="coerce")  # makes sure all values are treated as numbers
speed = speed.dropna()   # removes missing values if any exist
speed = speed[speed >= 0] # keeps only zero and positive wind speeds.

print(speed.head()) # prints the first 5 values
print(speed.shape)
print(speed.min(), speed.max())
u = speed - speed.mean() # creates the fluctuations around the mean, which is exactly what the assignment asks for in the autocorrelation formula.

print("\nThe list of fluctuation is :\n ", u.head()) # calculates the average wind speed.
print("the mean is: " ,u.mean())
acf_values = acf(u, nlags=336, fft=True)   #calculates autocorrelation values.means calculate autocorrelation from lag 0 to lag 336; since your data is hourly, 336 hours = 14 days.ffts is Faster method for long datasets

print("The autocorrelation values are: ",acf_values[:10]) # produces 10 values
print("The number of autocorrelation values are: ",len(acf_values))

table_15 = pd.DataFrame({
    "Lag (hours)": range(15),
    "Wind speed (m/s)": speed.iloc[:15].round(3).values,
    "Fluctuation u(t) (m/s)": u.iloc[:15].round(3).values,
    "Autocorrelation R(t)": acf_values[:15].round(3)
})  #range(15) gives lags 0 to 14. speed.iloc[:15] gives first 15 wind-speed values. u.iloc[:15] gives first 15 fluctuation values. acf_values[:15] gives first 15 autocorrelation values.


print(table_15)

lags = range(len(acf_values))

plt.figure(figsize=(10,5))
plt.plot(lags, acf_values)
plt.xlabel("Lag (hours)")
plt.ylabel("Autocorrelation R(t)")
plt.title("Autocorrelation of wind speed fluctuations")
plt.grid(True)
plt.show()


peaks, _ = find_peaks(acf_values[1:])   # ignore lag 0
peaks = peaks + 1
#These peak positions help you see the spacing between repeated peaks in the autocorrelation plot, and that spacing gives the oscillation period. If the peaks are about 24 lags apart, the period is about 24 hours.
print("\nThe locations of the peaks on the lag axis are ",peaks[:10])  #the locations of the peaks on the lag axis.
peak_diff = peaks[:10][1:] - peaks[:10][:-1]
print(peak_diff)
print("Average period =", round(peak_diff.mean(), 3), "hours")

max_lag_long = 24 * 365 * 1
lags_long = range(max_lag_long + 1)
autocorr_values_long = [u.autocorr(lag=lag) for lag in lags_long]
lags_days_long = [lag / 24 for lag in lags_long]
dt_days = 1 / 24
integral_time_scale = np.trapezoid(autocorr_values_long, dx=dt_days)
print("Integral time scale (days):", round(integral_time_scale, 3))

