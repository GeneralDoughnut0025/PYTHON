import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from windrose import (WindroseAxes, plot_windrose)     #### Instead of making the windrose from scratch i am calling it rom a package i found on the internet

df = pd.read_excel("SDF_i896_start_20170101_stripped.xlsx", header=None)
print("Original shape:", df.shape)

df = df.iloc[:, :4]
df.columns = ["date", "time", "direction_deg", "speed_ms"]

print(df.head())
print(df.shape)
print(
    df.info())  # will tell us whether Python read the columns as numbers or text and whether there are missing values.
df.columns = ["date", "time", "direction_deg",
              "speed_ms"]  # this is done to name each column so that referring to them in the code will be easier to understand instead of df[0] or df[0]
df = df.replace(["-----", "------", "---.-", "-.--"],
                np.nan)  # np.nan is a way of marking a value as missing when that value should have been a number.we are telling pandas, “this is not real data; treat it as missing.”
df["direction_deg"] = pd.to_numeric(df["direction_deg"],
                                    errors="coerce")  # Take the direction_deg column, makes it numeric, and if any value is not a valid number, marks it as missing (eg-NaN).
df["speed_ms"] = pd.to_numeric(df["speed_ms"],
                               errors="coerce")  # Takes the wind direction column, makes it numeric (2.2), and if any value is not a valid number, mark it as missing (eg-NaN)
# Basically, converting the column to numeric type. But during that conversion, it also checks each value and handles bad ones by turning them into NaN instead of throwing an error.
df_clean = df.dropna(subset=["direction_deg",
                             "speed_ms"])  # dropna() removes missing values. subset makes python only check these two columns. So if a row has missing direction or missing speed, that row is removed.
print(df_clean.head())
print(df_clean.shape)  # shape tells you the size of your table as a pair: (number_of_rows, number_of_columns)
print(df_clean.dtypes)  # shows the data type of each column in your DataFrame.

######### This is part 1b #########
#### the question is asking me to find the correlation there a plot will be used and figure out the whether speed changes with direction and to identify the dominant direction.
def part_1b():



        plt.figure(figsize=(10,10))                                        ##### we are making the plot here onwards.figure() means tells python to start a new blank figure for plotting.Matplotlib is the Python library used to make plots and charts, and pyplot is the plotting interface that creates figures, plotting areas, labels etc
        plt.scatter(df_clean["direction_deg"], df_clean["speed_ms"], s=8, alpha=0.4)  ##### x-axis is degree and y-axis speed, s=8 is the size of the points
        plt.xlabel("Wind direction (deg)")                                  #####The plotting helps to see whether higher wind speeds seem to happen more often at some directions.
        plt.ylabel("Wind speed (m/s)")
        plt.title("Degree VS Speed (m/s)")
        plt.show()

        ax = WindroseAxes.from_ax()                                           ##### SINCE, a simple scatter plot on xY axis is DIFFICULT TO READ, so we do a wind rose plot. Instead of making one from scratch we use a package found on teh web and just add our data.
        ax.bar(df_clean["direction_deg"], df_clean["speed_ms"], normed=True, opening=0.8, edgecolor="white")          #####ax.bar(...) tells the wind rose axis ax to make a  classic wind rose with circular sectors.normed=True shows frequency in normalized form, usually as percentages.  shows how common each direction-speed combination is relative to the whole dataset.opening=0.8 This controls the spacing between the bars.
        ax.set_legend()                                                       #####adds the legend to the wind rose, so you can see what the different colors mean for wind-speed ranges
        plt.show()                                                            ##### This is the plot support

        bins = np.arange(0, 361, 30)                    ## this is the mathematical support part.  not working with every single degree separately anymore;we are grouping directions into sectors such as 0–30°, 30–60°, 60–90°etc. By putting each observation into a 30-degree sector, you can calculate things like which sector has the largest frequency,  mean wind speed in each sector etc
        labels = ["0-30", "30-60", "60-90", "90-120", "120-150", "150-180", "180-210", "210-240", "240-270", "270-300", "300-330", "330-360"] ##list of names for the 12 sectors defined by your bins. Since bins has boundaries at 0,to 360, you need 12 labels to match the 12 intervals between those boundaries. The labels give each sector a readable name, so when you later group the data, the result is easier to understand
        df_clean["dir_bin"] = pd.cut(df_clean["direction_deg"], bins=bins, labels=labels, include_lowest=True, right=False) ##Python looks at the wind direction in each row, decide which 30-degree sector it belongs to, and save that sector name in a new column. df_clean["dir_bin"] creates a new column called dir_bin. bins.pd.cut(...) pandas function that places numeric values into intervals. bins=bins uses the bin boundaries created. labels=labels uses your readable names for those intervals.include_lowest=True makes sure the lowest boundary is included properly.right=False means each interval is left-closed and right-open, so 0-30 means 0≤x<30
        mean_speed_by_dir = df_clean.groupby("dir_bin")["speed_ms"].mean()    ##Take all rows in the same direction sector and find their average wind speed.df_clean-it is table that contains your usable wind data after cleaning.'.groupby("dir_bin")'-This tells pandas to split the table into groups based on the values in the dir_bin column (eg- all rows with dir_bin = "0-30" go together, then 30-60, etc). ["speed_ms"]-This selects only the speed_ms column from each group, after the grouping of direction is done now you tell python to conc on speed column. .mean()-calculates the average, for the selected speed_ms values in each group
        print(mean_speed_by_dir)

#### THIS IS CODE FOR 1C #####
def part_1c():
    df_clean["datetime"] = pd.to_datetime(df_clean["date"].astype(str) + " " + df_clean["time"].astype(str), errors="coerce")  #creates a new column called datetime by combining your date and time columns into one. autocorrelation is a time-series calculation, so your data must be arranged in time order.df_clean["date"] takes the date column. datetinme is a sata type like float and boolean
                                                                                                                               #.astype(str) changes the date values into text so they can be joined with the time values.(+ " ")- adds one space between date and time. df_clean["time"].astype(str) takes the time column and also converts it to text.
                                                                                                                                #pd.to_datetime(...) converts that combined text into real datetime values that pandas understands as time data. errors="coerce" means if some row has a bad date or time, pandas will not crash; it will turn that value into NaT, which means missing datetime.
    print("Number of ignored rows: "+ str(df_clean["datetime"].isna().sum()))                #isna() checks which values are missing, and sum() counts how many of those missing values there are
    print("Total rows:", len(df_clean))                                                      #this shows the total usable rows
    print(df_clean["datetime"].head(10))                                                     #I did this cause i wanted to see how the data looks, just curious
    df_time = df_clean.dropna(subset=["datetime"]).copy()                                    #.copy() - makes a new dataframe called df_time so you can work on it
    df_time = df_time.sort_values("datetime")                                                #.sort_values - This sorts the rows by the datetime column (from earliest to latest.).
    print(df_time[["datetime"]].head(10))                                                    #This prints the first 10 rows of the new datetime column.
    print(df_time[["datetime"]].tail(10))                                                    # gives the last ten rows
    df_time = df_time.set_index("datetime")                                                  #Makes datetime the row index instead of a normal column. Before, your rows are identified by normal integer positions like 0, 1, 2. After df_time =df_time.set_index("datetime"), each row is identified by a timestamp like 2015-12-07 14:50:00 instead.
    print(df_time.head())                                                                    #Shows the first 5 rows.
    print(df_time.index)                                                                     #index is a type check. print(df_time.index) to confirm pandas truly ecognized the index as datetime and not just as ordinary text or a regular index.
    speed = df_time["speed_ms"]                                                              #takes only the wind-speed column
    speed_fluct = speed - speed.mean()                                                       #subtracts the average wind speed from every value since ASSIGNMENT is asking us to work with mean fluctuations
    print(speed.head())
    print(speed_fluct.head())
    print("Mean wind speed:", speed.mean())
    max_lag = 14 * 24 * 6                                                                    # assignment says to compute autocorrelation for the municipality data for delays up to 14 or 24 days, and that municipality dataset is 10-minute average data(14 = 14 days as assignment asks for that, 24 = 24 hours in one day, 6 = 6 measurements per hour because your data is every 10 minutes, and 60/10=6.)
    lags = range(max_lag + 1)                                                                # creates a sequence of whole numbers starting at 0 and increasing by 1, and Python stops just before the number you give to range().lag = 1 means 10 minutes, lag = 6 means 1 hour, and lag = 2016 means 14 days.
    autocorr_values = [speed_fluct.autocorr(lag=lag) for lag in lags]                        # for every lag value, calculate the autocorrelation, then store all the answers in a list. autocorr_values is just the name of the variable.[ ... ] means Python should build a list from the values produced inside it.for lag in lags means Python goes through each lag value one by one. .autocorr(...) calls the pandas autocorrelation function, and the parentheses are what actually run the function, correlation between the series and a shifted version of itself.lag=lag means “use the current lag value from the loop” when calculating autocorrelation.
    lags_days = [lag / (6 * 24) for lag in lags]                                             # converts lag numbers into days, municipality data has 6 measurements per hour, so dividing by (6*24) converts lag steps to days.
    plt.figure(figsize=(24, 10))                                                             ### GRAPH of days vs autocorrelation
    plt.plot(lags_days, autocorr_values)                                               ### we plot to see whether it oscillates, estimate the period of that oscillation, as 1c also asks us to do that. Just the numerical values would be difficult.
    plt.xlabel("Days")
    plt.ylabel("Autocorrelation")
    plt.title("Autocorrelation of wind speed fluctuations")
    plt.xticks(np.arange(0, 14.5, 0.5))
    plt.yticks(np.arange(1, -0.02, -0.02))
    plt.grid(True)
    plt.show()
    acf_table = pd.DataFrame({
        "lag": list(lags),
        "lag_days": [lag / (6 * 24) for lag in lags],
        "autocorrelation": autocorr_values
    })                                                                                        ##### This is to get a table and look  at the autocorrelation every 0.5 day
    print(acf_table.iloc[::72])                                                               ##### 0.5 day = 72 lags, .iloc- This tells pandas to select rows by their row number position. [::72]- so start from the first row, go to the last row and take one row then skip 71 rows and  then take the next. It is better than printing all 2017 riws and inspecting.


    max_lag_long = 6 * 24 * 80                                                                ### this is where part 1 c2 starts, Since i am asked to find the area under the correlation plot and the assignment asks me use a longer time period, thats why i am using a 80 days. Everything is the same as c1. just a longer time period.
    lags_long = range(max_lag_long + 1)
    autocorr_values_long = [speed_fluct.autocorr(lag=lag) for lag in lags_long]
    lags_days_long = [lag / (6 * 24) for lag in lags_long]
    dt_days = 10 / (60 * 24)                                                                  ### this converts sampling interval from 10 minutes into days. Since lag axis for c2 is being treated in days, the spacing must also be in days.
    integral_time_scale = np.trapezoid(autocorr_values_long, dx=dt_days)                          ### autocorr_values_long is your list of autocorrelation values. (np.trapz)- estimates the area under the curve. dx=dt_days- dx tells np.trapz how far apart your autocorrelation points are on the x-axis
    print("Integral time scale (days): ", integral_time_scale)                                ### autocorr_values_long is the heights of the curve (y-axis) while, dx provides that width (x-axis).



part_1c()
part_1b()










