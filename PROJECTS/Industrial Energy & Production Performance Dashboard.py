##Project title: Industrial Energy & Production Performance Dashboard
##  SELF PROJECT
#Part 1: Analysis :: energy per unit produced,downtime vs energy waste & shift-wise KPI trends.
#Part 2 ::: Monitoring, detect unusual spikes in power use,flag abnormal machine behavior, simple threshold or anomaly detection model.
#Part 3 :::: Optimization, what-if tool: “what happens if runtime shifts to cheaper tariff hours?” estimate savings in cost, kWh, and emissions.

## PART 1
# Part 1: Industrial Energy & Production Performance Dashboard
# This script performs production and downtime analysis on the factory dataset.

import pandas as pd  # pandas is used for reading, cleaning, and analyzing tabular data.
import matplotlib.pyplot as plt  # matplotlib is used for making charts.
pd.set_option("display.max_columns", None)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.width", 1000)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.max_colwidth", None) ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY



# Read the Excel file into a DataFrame named df.
# pd.read_excel(...) loads spreadsheet data into rows and columns we can work with in Python.
df = pd.read_excel(r"C:\Users\Reaga\Downloads\factory_energy_data.xlsx", sheet_name="Sheet1")
# Convert the date column from plain text/Excel date format into a real datetime type.
# pd.to_datetime(...) makes time-based grouping, sorting, and filtering easier.
df["date"] = pd.to_datetime(df["date"])

# Convert shift values to strings so labels like 1 and 2 behave consistently in charts and groupings.
# astype(str) changes the data type of the entire column.
df["shift"] = df["shift"].astype(str)

# Extract only the numeric part from values like "7 kg" or "8 kg".
# .str.extract(r"(\d+)") uses a regular expression to capture one or more digits.
# astype(float) changes the extracted text into numbers.
df["cabinet_kg_num"] = df["cabinet_size_Kg"].astype(str).str.extract(r"(\d+)").astype(float)

# Create yield percentage = good units divided by order quantity.
# New columns are created with df["new_column"] = ... syntax.
df["yield_pct"] = df["good_units"] / df["order_qty"]

# Create scrap percentage = scrap units divided by order quantity.
df["scrap_pct"] = df["scrap_units"] / df["order_qty"]

# Create a simple waste proxy combining scrap and downtime.
# This is not true energy data, but it is a useful operational-loss indicator.
df["waste_proxy"] = df["scrap_units"] + df["total_downtime_min"]

# Print a quick preview so we can inspect the first five rows.
# head() returns the top rows of a DataFrame.
print(df.head())

# -----------------------------
# OVERALL KPI SUMMARY
# -----------------------------

# Sum the full order quantity column.
total_order_qty = df["order_qty"].sum()

# Sum the total good units produced.
total_good_units = df["good_units"].sum()

# Sum the total scrap units produced.
total_scrap_units = df["scrap_units"].sum()

# Sum the total downtime minutes.
total_downtime = df["total_downtime_min"].sum()

# Compute overall yield percentage across the full dataset.
overall_yield = total_good_units / total_order_qty

# Compute overall scrap percentage across the full dataset.
overall_scrap = total_scrap_units / total_order_qty

# Print the summary KPIs.
print("\n=== OVERALL KPI SUMMARY ===")
print("Total order quantity:", total_order_qty)
print("Total good units:", total_good_units)
print("Total scrap units:", total_scrap_units)
print("Total downtime (min):", total_downtime)
print("Overall yield %:", round(overall_yield * 100, 2))
print("Overall scrap %:", round(overall_scrap * 100, 2))

# -----------------------------
# SHIFT-WISE KPI TRENDS
# -----------------------------

# groupby("shift") splits the dataset into one group per shift.
# agg(...) calculates multiple summary measures for each group.
shift_kpis = df.groupby("shift").agg(
    runs=("shift", "count"),
    order_qty=("order_qty", "sum"),
    good_units=("good_units", "sum"),
    scrap_units=("scrap_units", "sum"),
    breakdown_min=("downtime_breakdown_min", "sum"),
    changeover_min=("downtime_changeover_min", "sum"),
    total_downtime_min=("total_downtime_min", "sum")
).reset_index()

# Add calculated percentages after aggregation.
shift_kpis["yield_pct"] = shift_kpis["good_units"] / shift_kpis["order_qty"]
shift_kpis["scrap_pct"] = shift_kpis["scrap_units"] / shift_kpis["order_qty"]
shift_kpis["avg_downtime_per_run"] = shift_kpis["total_downtime_min"] / shift_kpis["runs"]

# Print the shift-wise KPI table.
print("\n=== SHIFT-WISE KPIs ===")
print(shift_kpis)

# -----------------------------
# CABINET SIZE ANALYSIS
# -----------------------------

# Group by cabinet size to compare which size performs better or worse.
cabinet_kpis = df.groupby("cabinet_kg_num").agg(
    runs=("cabinet_kg_num", "count"),
    order_qty=("order_qty", "sum"),
    good_units=("good_units", "sum"),
    scrap_units=("scrap_units", "sum"),
    total_downtime_min=("total_downtime_min", "sum")
).reset_index()

# Create cabinet-level percentages.
cabinet_kpis["yield_pct"] = cabinet_kpis["good_units"] / cabinet_kpis["order_qty"]
cabinet_kpis["scrap_pct"] = cabinet_kpis["scrap_units"] / cabinet_kpis["order_qty"]

# Sort cabinet sizes in increasing numeric order.
cabinet_kpis = cabinet_kpis.sort_values("cabinet_kg_num")

# Print the cabinet comparison table.
print("\n=== CABINET SIZE KPIs ===")
print(cabinet_kpis)

# -----------------------------
# MONTHLY TREND ANALYSIS
# -----------------------------

# Create a month column using datetime periods like 2026-01, 2026-02, etc.
df["month"] = df["date"].dt.to_period("M").astype(str)

# Group by month to see trend movement over time.
monthly_kpis = df.groupby("month").agg(
    order_qty=("order_qty", "sum"),
    good_units=("good_units", "sum"),
    scrap_units=("scrap_units", "sum"),
    total_downtime_min=("total_downtime_min", "sum"),
    waste_proxy=("waste_proxy", "sum")
).reset_index()

# Add monthly rates.
monthly_kpis["yield_pct"] = monthly_kpis["good_units"] / monthly_kpis["order_qty"]
monthly_kpis["scrap_pct"] = monthly_kpis["scrap_units"] / monthly_kpis["order_qty"]

# Print the monthly KPI table.
print("\n=== MONTHLY KPIs ===")
print(monthly_kpis)

# -----------------------------
# MACHINE BREAKDOWN ANALYSIS
# -----------------------------

# Reshape the three machine breakdown columns into a long format.
# melt(...) turns multiple machine columns into two columns: machine name and flag value.
machine_flags = df.melt(
    id_vars=["date", "shift"],
    value_vars=["machine1_breakdown", "machine2_breakdown", "machine3_breakdown"],
    var_name="machine",
    value_name="breakdown_flag"
)

# Count how many YES values appear for each machine.
machine_summary = machine_flags.groupby("machine").agg(
    total_records=("breakdown_flag", "count"),
    yes_count=("breakdown_flag", lambda x: (x.str.upper() == "YES").sum())
).reset_index()

# Calculate the percentage of YES breakdown flags.
machine_summary["breakdown_rate"] = machine_summary["yes_count"] / machine_summary["total_records"]

# Print the machine-level summary.
print("\n=== MACHINE BREAKDOWN SUMMARY ===")
print(machine_summary)


# -----------------------------
# CHART 1: SHIFT-WISE KPI BAR CHART
# -----------------------------

# Create a figure canvas and define its size in inches.
plt.figure(figsize=(8, 5))

# Plot good units by shift as a bar chart.
plt.bar(shift_kpis["shift"], shift_kpis["good_units"])

# Add chart title and axis labels.
plt.title("Good Units by Shift")
plt.xlabel("Shift")
plt.ylabel("Good Units")

# Adjust layout so labels do not get cut off.
plt.tight_layout()

# -----------------------------
# CHART 2: MONTHLY DOWNTIME VS SCRAP TREND
# -----------------------------

# Create another chart canvas.
plt.figure(figsize=(9, 5))

# Plot total downtime by month as a line.
plt.plot(monthly_kpis["month"], monthly_kpis["total_downtime_min"], marker="o", label="Total Downtime (min)")

# Plot scrap units by month as another line.
plt.plot(monthly_kpis["month"], monthly_kpis["scrap_units"], marker="s", label="Scrap Units")

# Add title, labels, and legend.
plt.title("Monthly Downtime vs Scrap Trend")
plt.xlabel("Month")
plt.ylabel("Value")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()


# -----------------------------
# CHART 3: CABINET SIZE SCRAP PERCENTAGE
# -----------------------------

# Create a third chart canvas.
plt.figure(figsize=(8, 5))

# Plot scrap percentage by cabinet size.
plt.bar(cabinet_kpis["cabinet_kg_num"].astype(str), cabinet_kpis["scrap_pct"] * 100)

# Add title and labels.
plt.title("Scrap Percentage by Cabinet Size")
plt.xlabel("Cabinet Size (kg)")
plt.ylabel("Scrap %")
plt.tight_layout()
plt.show()
print(df.head().to_string())  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY




## yield_pct:: This means production yield percentage: the share of total output that became good units.
# In real life, it tells you how efficiently the line turned orders into usable product.
##scrap_pct::: This means scrap percentage: the share of total output that became scrap.
# In real life, it shows how much production was wasted and could not be sold or used.
##waste_proxy:: This is not a standard manufacturing KPI name, but in your code it is a simple loss indicator built from, scrap_units + total_downtime_min.
#In real life, it is a rough way to combine two kinds of loss:scrap_units = product waste + total_downtime_min = time waste.



##-------------------------------------------------------------------------------------------------------------------
####  Part 2 is Operational Monitoring & Anomaly Detection.
##-------------------------------------------------------------------------------------------------------------------


# Create scrap percentage if it is not already there.
if "scrap_pct" not in df.columns:
    df["scrap_pct"] = df["scrap_units"] / df["order_qty"]

# Create a simple loss score from scrap and downtime.
df["loss_score"] = df["scrap_units"] + df["total_downtime_min"]

# Convert machine breakdown YES/NO flags into numeric 1/0 values.
df["machine1_flag"] = (df["machine1_breakdown"].astype(str).str.upper() == "YES").astype(int)
df["machine2_flag"] = (df["machine2_breakdown"].astype(str).str.upper() == "YES").astype(int)
df["machine3_flag"] = (df["machine3_breakdown"].astype(str).str.upper() == "YES").astype(int)

# Count how many machines showed breakdown in the same run.
df["machine_breakdown_count"] = df[["machine1_flag", "machine2_flag", "machine3_flag"]].sum(axis=1)

# Calculate z-scores for downtime, scrap, and loss score.
# A z-score tells you how far a value is from the average, in units of standard deviation.
##Z-scores are useful for outlier detection because they make it easy to spot values that stand out from the normal pattern.
# In your code, they help support the idea of “unusual spikes” in production loss or downtime.
df["downtime_z"] = (df["total_downtime_min"] - df["total_downtime_min"].mean()) / df["total_downtime_min"].std()
df["scrap_z"] = (df["scrap_units"] - df["scrap_units"].mean()) / df["scrap_units"].std()
df["loss_score_z"] = (df["loss_score"] - df["loss_score"].mean()) / df["loss_score"].std()

# Set simple thresholds using the 95th percentile.--We do this to detect unusual spikes without needing a complicated model. Percentile thresholds are simple, easy to explain, and they work even if the data is not perfectly normal.
##This part sets cutoff values using the 95th percentile.---You are right that values above the 95th percentile are not guaranteed to be “bad” or “weird.” They are simply the most unusual compared with the rest of your data. That means percentile cutoffs are a practical rule, not a perfect truth.
# It means anything above those cutoffs is treated as unusually high and may be flagged as a spike or abnormal event.
##Your code uses the 95th percentile because it is trying to catch the worst 5% of downtime, scrap, and loss-score values.
# That is a simple way to find likely problem runs without making the script too complicated.
##Think of it like setting an alarm ::: too low a cutoff means the alarm goes off all the time, too high a cutoff means you miss problems and 95th percentile is a middle ground.
downtime_threshold = df["total_downtime_min"].quantile(0.95)
scrap_threshold = df["scrap_units"].quantile(0.95)
loss_score_threshold = df["loss_score"].quantile(0.95)

# Flag rows that exceed the thresholds.
df["downtime_spike_flag"] = df["total_downtime_min"] > downtime_threshold  ##This checks every row :::: if downtime is above the threshold, it becomes True otherwise it becomes False
df["scrap_spike_flag"] = df["scrap_units"] > scrap_threshold  # they store True or False for each row.
df["loss_spike_flag"] = df["loss_score"] > loss_score_threshold
df["abnormal_machine_flag"] = df["machine_breakdown_count"] == 3 #It does not compare to a percentile threshold. Instead, it checks whether all 3 machines broke down in the same run.

# Combine the flags into one anomaly score.
df["anomaly_score"] = (
    df["downtime_spike_flag"].astype(int) +
    df["scrap_spike_flag"].astype(int) +
    df["loss_spike_flag"].astype(int) +
    df["abnormal_machine_flag"].astype(int)
)  ##That line adds up how many flags are True in each row and stores the total as a number.True becomes 1 after .astype(int).

# Turn the anomaly score into a risk label.that block is the rule set that decides whether a row is Normal, Warning, or Critical.
# It checks the anomaly_score and assigns a label based on the number of flags that were triggered
def label_risk(score):
    if score >= 3:
        return "Critical"
    elif score >= 1:
        return "Warning"
    return "Normal"

df["risk_label"] = df["anomaly_score"].apply(label_risk)  ##This applies the label_risk() function to every row in the anomaly_score column and writes the result into a new column called risk_label.
# In other words, it takes each score and converts it into a text label.

# Print thresholds.
print("\n=== PART 2 MONITORING THRESHOLDS ===")
print("Downtime 95th percentile threshold:", downtime_threshold)
print("Scrap 95th percentile threshold:", scrap_threshold)
print("Loss score 95th percentile threshold:", loss_score_threshold)

# Summary of risk labels.
risk_summary = df["risk_label"].value_counts().reset_index()
risk_summary.columns = ["risk_label", "count"]
print("\n=== RISK LABEL SUMMARY ===")
print(risk_summary.to_string(index=False))

# Keep only warning and critical rows.
flagged_runs = df[df["anomaly_score"] >= 1].copy()
flagged_runs = flagged_runs.sort_values(
    by=["anomaly_score", "loss_score", "total_downtime_min", "scrap_units"],
    ascending=[False, False, False, False]
)

print("\n=== TOP FLAGGED RUNS ===")
print(flagged_runs[[
    "date", "shift", "cabinet_size_Kg", "order_qty", "good_units", "scrap_units",
    "total_downtime_min", "machine_breakdown_count", "anomaly_score", "risk_label"
]].head(20).to_string(index=False))

# Monthly monitoring summary.
monthly_monitoring = df.groupby("month").agg(
    runs=("date", "count"),
    avg_scrap_units=("scrap_units", "mean"),
    avg_downtime_min=("total_downtime_min", "mean"),
    warning_or_critical_runs=("anomaly_score", lambda x: (x >= 1).sum()),
    critical_runs=("risk_label", lambda x: (x == "Critical").sum())
).reset_index()

print("\n=== MONTHLY MONITORING SUMMARY ===")
print(monthly_monitoring.to_string(index=False))

# -----------------------------
# CHART 1: DOWNTIME WITH FLAGGED RUNS
# -----------------------------
###
## The middle of the y-axis is not the mean. The y-axis is just the scale of values, so the center is only the middle of the displayed range; the mean could be anywhere on that scale.
## The dots mark the flagged runs — the rows your code labeled as unusual because they crossed the threshold you set.
## The blue line is the full time series: in the first chart, it shows downtime across dates, in the second chart, it shows scrap across dates.
#  The line is there so you can see the overall movement over time, while the dots highlight the rows your code flagged.
plt.figure(figsize=(11, 5))
plt.plot(df["date"], df["total_downtime_min"], label="Total Downtime (min)")
plt.scatter(flagged_runs["date"], flagged_runs["total_downtime_min"], color="red", label="Flagged Runs")
plt.title("Downtime Monitoring with Flagged Runs")
plt.xlabel("Date")
plt.ylabel("Downtime (min)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# -----------------------------
# CHART 2: SCRAP WITH FLAGGED RUNS
# -----------------------------
plt.figure(figsize=(11, 5))
plt.plot(df["date"], df["scrap_units"], label="Scrap Units")
plt.scatter(flagged_runs["date"], flagged_runs["scrap_units"], color="orange", label="Flagged Runs")
plt.title("Scrap Monitoring with Flagged Runs")
plt.xlabel("Date")
plt.ylabel("Scrap Units")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# -----------------------------
# CHART 3: MONTHLY WARNING/CRITICAL RUNS
# -----------------------------
plt.figure(figsize=(9, 5))
plt.bar(monthly_monitoring["month"], monthly_monitoring["warning_or_critical_runs"])
plt.title("Monthly Warning or Critical Runs")
plt.xlabel("Month")
plt.ylabel("Flagged Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



##-------------------------------------------------------------------------------------------------------------------
# PART 3: OPTIMIZATION
##-------------------------------------------------------------------------------------------------------------------


# Create simple what-if improvement assumptions.
# You can change these percentages later if needed.
scrap_reduction_pct = 0.10          # assume scrap can be reduced by 10%
downtime_reduction_pct = 0.15       # assume downtime can be reduced by 15%

# Estimate improved scrap and downtime after optimization. - ake the current scrap units,
## those are just formulas, and they use the same DataFrame (df) from your earlier code, not a new file.
# They create new columns by taking the old values and reducing them by the assumed percentages.
df["optimized_scrap_units"] = df["scrap_units"] * (1 - scrap_reduction_pct)
df["optimized_total_downtime_min"] = df["total_downtime_min"] * (1 - downtime_reduction_pct)

# Estimate scrap units saved and downtime minutes saved.
df["scrap_units_saved"] = df["scrap_units"] - df["optimized_scrap_units"]
df["downtime_minutes_saved"] = df["total_downtime_min"] - df["optimized_total_downtime_min"]

# Assume reduced scrap becomes additional good output.
df["optimized_good_units"] = df["good_units"] + df["scrap_units_saved"]

# Recalculate basic performance rates after optimization.
df["optimized_yield_pct"] = df["optimized_good_units"] / df["order_qty"]
df["optimized_scrap_pct"] = df["optimized_scrap_units"] / df["order_qty"]

# Improve the same loss proxy you used earlier.
df["optimized_waste_proxy"] = df["optimized_scrap_units"] + df["optimized_total_downtime_min"]
df["waste_proxy_reduction"] = df["waste_proxy"] - df["optimized_waste_proxy"]

# -----------------------------
# OVERALL OPTIMIZATION SUMMARY
# -----------------------------
total_scrap_before = df["scrap_units"].sum()
## df["optimized_scrap_units"] = df["scrap_units"] * (1 - scrap_reduction_pct) calculates a new value for each row.
##total_scrap_before = df["scrap_units"].sum() adds up all scrap values together into one total number.
## same logic for the rest
total_scrap_after = df["optimized_scrap_units"].sum()

total_downtime_before = df["total_downtime_min"].sum()
total_downtime_after = df["optimized_total_downtime_min"].sum()
total_good_before = df["good_units"].sum()
total_good_after = df["optimized_good_units"].sum()
overall_yield_before = df["good_units"].sum() / df["order_qty"].sum()
overall_yield_after = df["optimized_good_units"].sum() / df["order_qty"].sum()
overall_scrap_before = df["scrap_units"].sum() / df["order_qty"].sum()
overall_scrap_after = df["optimized_scrap_units"].sum() / df["order_qty"].sum()


print("\n=== PART 3 OPTIMIZATION SUMMARY ===")
## those lines just display the values on screen. They do not change the data; they simply print the numbers so you can read them.
# The round(..., 2) part rounds the number to 2 decimal places before printing.
print("Total scrap units before:", round(total_scrap_before, 2))
print("Total scrap units after:", round(total_scrap_after, 2))
print("Scrap units saved:", round(df["scrap_units_saved"].sum(), 2))
print("Total downtime before:", round(total_downtime_before, 2))
print("Total downtime after:", round(total_downtime_after, 2))
print("Downtime minutes saved:", round(df["downtime_minutes_saved"].sum(), 2))
print("Good units before:", round(total_good_before, 2))
print("Good units after:", round(total_good_after, 2))
print("Extra good units gained:", round(df["scrap_units_saved"].sum(), 2))
print("Overall yield before %:", round(overall_yield_before * 100, 2))
print("Overall yield after %:", round(overall_yield_after * 100, 2))
print("Overall scrap before %:", round(overall_scrap_before * 100, 2))
print("Overall scrap after %:", round(overall_scrap_after * 100, 2))
print("Waste proxy reduction:", round(df["waste_proxy_reduction"].sum(), 2))

# -----------------------------
# SHIFT-WISE OPTIMIZATION SUMMARY
# -----------------------------

## shift_optimization is a summary table for each shift.
# It groups the rows by shift and then calculates totals for scrap, downtime, good units, and waste proxy so you can compare Shift 1 and Shift 2 side by side
##df.groupby("shift") splits the dataset into groups based on the shift column. After that, the code applies summary calculations to each group
#.agg(...) means aggregate. It lets you run several summary functions at once, like ::: sum for totals, count for number of runs.
#runs: how many rows/runs belong to that shift...... scrap_before: total scrap in that shift before optimization.......  scrap_after: total optimized scrap in that shift after your assumed improvement......scrap_saved: how much scrap was reduced.......
# downtime_after: total downtime after optimization...... downtime_saved: how many downtime minutes were saved...... downtime_before: total downtime before optimization......
# good_before: total good units before optimization...... good_after: total good units after optimization..... waste_proxy_before: original combined loss score.   ... waste_proxy_after: improved combined loss score.
shift_optimization = df.groupby("shift").agg(
    runs=("shift", "count"),
    scrap_before=("scrap_units", "sum"),
    scrap_after=("optimized_scrap_units", "sum"),
    scrap_saved=("scrap_units_saved", "sum"),
    downtime_before=("total_downtime_min", "sum"),
    downtime_after=("optimized_total_downtime_min", "sum"),
    downtime_saved=("downtime_minutes_saved", "sum"),
    good_before=("good_units", "sum"),
    good_after=("optimized_good_units", "sum"),
    waste_proxy_before=("waste_proxy", "sum"),
    waste_proxy_after=("optimized_waste_proxy", "sum")
).reset_index()
##These calculate the yield percentage for each shift : before optimization and after optimization.
#They divide good units by total order quantity for that same shift. So if a shift made 900 good units out of 1,000 ordered, its yield is 90%.
## This table helps you answer: Which shift improves more after the optimization scenario? It turns the row-level data into a shift-level comparison, which is easier to present in a report.
shift_optimization["yield_before_pct"] = shift_optimization["good_before"] / df.groupby("shift")["order_qty"].sum().values # good units before optimization ÷ total order quantity for that shift
shift_optimization["yield_after_pct"] = shift_optimization["good_after"] / df.groupby("shift")["order_qty"].sum().values # good units after optimization ÷ total order quantity for that shift.

# These just display the whole summary table in the console in a clean format, without row numbers. They do not change the data.
print("\n=== SHIFT-WISE OPTIMIZATION SUMMARY ===")
print(shift_optimization.to_string(index=False))

# -----------------------------
# CABINET SIZE OPTIMIZATION SUMMARY
# -----------------------------
cabinet_optimization = df.groupby("cabinet_kg_num").agg(
    runs=("cabinet_kg_num", "count"),
    scrap_before=("scrap_units", "sum"),
    scrap_after=("optimized_scrap_units", "sum"),
    scrap_saved=("scrap_units_saved", "sum"),
    downtime_before=("total_downtime_min", "sum"),
    downtime_after=("optimized_total_downtime_min", "sum"),
    downtime_saved=("downtime_minutes_saved", "sum"),
    good_before=("good_units", "sum"),
    good_after=("optimized_good_units", "sum")
).reset_index().sort_values("cabinet_kg_num")

print("\n=== CABINET SIZE OPTIMIZATION SUMMARY ===")
print(cabinet_optimization.to_string(index=False))

# -----------------------------
# MONTHLY OPTIMIZATION SUMMARY
# -----------------------------
monthly_optimization = df.groupby("month").agg(
    scrap_before=("scrap_units", "sum"),
    scrap_after=("optimized_scrap_units", "sum"),
    scrap_saved=("scrap_units_saved", "sum"),
    downtime_before=("total_downtime_min", "sum"),
    downtime_after=("optimized_total_downtime_min", "sum"),
    downtime_saved=("downtime_minutes_saved", "sum"),
    good_before=("good_units", "sum"),
    good_after=("optimized_good_units", "sum"),
    waste_proxy_before=("waste_proxy", "sum"),
    waste_proxy_after=("optimized_waste_proxy", "sum")
).reset_index()

print("\n=== MONTHLY OPTIMIZATION SUMMARY ===")
print(monthly_optimization.to_string(index=False))

# -----------------------------
# CHART 1: MONTHLY DOWNTIME BEFORE VS AFTER
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(monthly_optimization["month"], monthly_optimization["downtime_before"], marker="o", label="Downtime Before")
plt.plot(monthly_optimization["month"], monthly_optimization["downtime_after"], marker="s", label="Downtime After")
plt.title("Monthly Downtime Before vs After Optimization")
plt.xlabel("Month")
plt.ylabel("Downtime (min)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# -----------------------------
# CHART 2: MONTHLY SCRAP BEFORE VS AFTER
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(monthly_optimization["month"], monthly_optimization["scrap_before"], marker="o", label="Scrap Before")
plt.plot(monthly_optimization["month"], monthly_optimization["scrap_after"], marker="s", label="Scrap After")
plt.title("Monthly Scrap Before vs After Optimization")
plt.xlabel("Month")
plt.ylabel("Scrap Units")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# -----------------------------
# CHART 3: SHIFT-WISE WASTE REDUCTION
# -----------------------------
plt.figure(figsize=(8, 5))
plt.bar(
    shift_optimization["shift"].astype(str),
    shift_optimization["waste_proxy_before"] - shift_optimization["waste_proxy_after"]
)

##This graph shows waste proxy reduction by shift after your Part 3 what-if improvement.
# The taller the bar, the more total waste reduction that shift would get from the assumed optimization. The numbers 1 and 2 on the x-axis are just the two shift values in your dataset.
## Each bar shows the total reduction in your waste_proxy for that shift. Since waste_proxy was defined as scrap_units + total_downtime_min, the bar represents the combined improvement in scrap and downtime under your optimization scenario.
plt.title("Waste Proxy Reduction by Shift")
plt.xlabel("Shift")
plt.ylabel("Waste Proxy Reduction")
plt.tight_layout()

plt.show()










