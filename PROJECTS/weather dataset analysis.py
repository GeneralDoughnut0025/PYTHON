#DATA ANALYSIS 1-- weather dataset
import pandas as pd
pd.set_option("display.max_columns", None)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.width", 1000)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.max_colwidth", None) ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
from sympy.codegen import Print


data=pd.read_csv(r"C:\Users\Reaga\Downloads\1. Weather Data.csv")
print("\nTHIS IS THE FIRST 5 DATA: ")
print(data.head())
print("\nTHIS IS ALL THE DATA: ")
print(data)
print(f"\nThere are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.")

print(f"\nTHE COLUMN NAMES ARE:")
print(data.columns)

print(f"\nTHE DATA TYPE OF EACH COLUMN IS: ")
print(data.dtypes)

print(f"\nTHE TOTAL NUMBER OF UNIQUE VALUES IN EACH COLUMN IS: ")
print(data.nunique())

print(f"\nIN THE WEATHER COLUMN THE UNIQUE VALUES, ALONG WITH THEIR COUNT IS: ")
print(data['Weather'].value_counts())

print(f"\nTHE DATA INFO IS: ")
print(data.info())

#FINDING UNIQUE VALUES IN THE 'WIND SPEED' COLUMN
print(f"\nTHE NUMBER OF UNIQUE VALUES IN WIND SPEED IS: {data['Wind Speed_km/h'].nunique()}")
print(f"THE UNIQUE DATA IS: {data['Wind Speed_km/h'].unique()}")

#FINDING THE NUMBER OF TIMES THE WEATHER IS EXACTLY CLEAR
print(f"\nTHESE ARE THE NUMBER OF VARIOUS WEATHER REPORTS:")
print(data['Weather'].value_counts())
#TO MAKE A NEW DATASET OF ONLY CLEAR
data[data.Weather == 'Clear']

#TO MAKE A NEW DATASET OF ONLY IND SPEED4 Km/hr
print(f"THESE ARE THE DAYS WHERE WIND SPEED IS 4Km/hr: ")
print(data[data['Wind Speed_km/h'] == 4])

#FINDING THE NUMBER OF NULL VALUES
print(f"\n THE NUMBER OF NULL VALUES IN EACH COLUMN ARE: \n{data.isnull().sum()}")

#RENAMING THE WEATHER COLUMN TO WEATHER CONDITION
data.rename(columns={'Press_kPa':'Pressure in Kilo Pascals'}, inplace=True)
print(data.head())

#TO FIND THE MEAN OF VISIBILITY COLUMN
print(f"\n THE MEAN OF VISIBILITY IS : {data.Visibility_km.mean():.4f} ")  #THE :.4f Tells the number of decimal points after

#TO FIND THE STANDARD DEVIATION OF PRESSURE AND VARIANCE IN REL HUMIDITY
print(f"\nTHE STD DEVIATION IS: {data['Pressure in Kilo Pascals'].std():.3f} AND THE VARIANCE IN REL HUMIDITY IS: {data['Rel Hum_%'].var():.3f}")

#finding the instances when snow was recorded
snow_exact_count = data[data['Weather'].str.contains('Snow')]
print(f"Number of exact 'Snow' records:\n{snow_exact_count}\n and the total number is {data[data['Weather'].str.contains('Snow')].shape[0]}")

#   FIMD OUT WHEN SPEED IS ABOVE 24 AND VISIBILITY IS 25
result = data[(data['Wind Speed_km/h'] > 24) & (data['Visibility_km'] == 25)]
print(f"\nNumber of times wind speed was above 24 and visibility was 25: {result.shape[0]}")
result = data[(data['Wind Speed_km/h'] > 24) & (data['Visibility_km'] == 25)]
print(f"the rows are:\n{result}")

#MEAN OF EACH WEATHER CONDITION:
mean_weather = data.groupby('Weather').mean(numeric_only=True)
print(mean_weather)

#minimum and maximum value of each column against each weather condition
print(data.groupby('Weather').agg(['min', 'max']))

#RECORDS WHERE WEATHER CONDITIION IS FOG
fog_count = data[data['Weather'].str.contains('Fog', na=False)].shape[0]
print(f"Number of records where weather condition is Fog: {fog_count}")
fog_rows = data[data['Weather'].str.contains('Fog', na=False)]
print(fog_rows)
print(data.head().to_string())

