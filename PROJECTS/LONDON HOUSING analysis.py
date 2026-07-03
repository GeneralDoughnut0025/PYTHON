# DATA ANALYSIS-LONDON HOUSING DATA
import pandas as pd
import numpy as np
pd.set_option("display.max_columns", None)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.width", 1000)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.max_colwidth", None) ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY ## THIS WILL GIVE ALL THE COLUMNS INSTEAD OF "...."
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv(r"C:\Users\Reaga\Downloads\5. London Housing Data.csv")
print(f"the number of data is : \n {data.count()}") #tells the number of data in each column
print(f"The number of null values in each column is:\n{data.isnull().sum()}")#That gives the number of missing values per column.Null values are missing or blank data points in your dataset.

def missing_heatmap(df):  #THIS IS THE HEATMAP CODE AND I USED THE CALLING FUNCTION TO MAKE IT COOLER
    plt.figure(figsize=(10, 5))
    sns.heatmap(data.isnull(), cbar=True, yticklabels=False, cmap='viridis')
    plt.title('Missing Values Heatmap')
    plt.xlabel('Columns')
    plt.ylabel('Rows / Records')
    plt.show()  ##
missing_heatmap(data)  #THIS IS THE HEATMAP CODE AND I USED THE CALLING FUNCTION TO MAKE IT COOLER

#NOW WE CONVERT THE DATATYPE OF 'DATE' COLUMN TO DATE-TIME FORMAT
data.head() #this just gives the first 5 rows of our data
data.dtypes#TO CHECK THE TYPES OF THE DATA
data.date=pd.to_datetime(data.date)
data.dtypes # THIS IS THE NEW DATA TYPE FOR DATE AFTER WE CHANGED IT

print(data.head().to_string())  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY

##NOW WE MUST ADD A NEW COLUMN CALLED YEAR. THIS IS AT THE END, IE THE LAST COLUMNS
data['year']=data.date.dt.year
print(data.head())

# NOW WE WANT TO ADD A COLUMN 'DATE' BETWEEN YEAR AND CITY
data.insert(1, 'month', data.date.dt.month)
print(data.head())

#REMOVING THE COLUMNS OF YEAR AND MONTH
data.drop(['month','year'], axis=1, inplace=True)
print(data.head())

#SHOW ALL RECORDS WHERE CRIME IS 0 AND HOW MANY SUCH RECORDS ARE THERE
zero_crimes=data[data.no_of_crimes == 0]
print(zero_crimes)
print(zero_crimes.shape[0]) ## this just gives the number of rows, if [0] is not there it will return rows and columns

#MAX AND MIN 'AVERAGE PRICE' PER YEAR IN ENGLAND
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['year'] = data.date.dt.year
england=data[data.area=='england']
print(f"THE MAX FROM EACH YEAR IS:\n {data.groupby('year').average_price.max()}")
print(f"THE MIN FROM EACH YEAR IS:\n {data.groupby('year').average_price.min()}")
print(f"THE MAX FROM EACH YEAR IN ENGLAND IS:\n {england.groupby('year').average_price.max()}")
print(f"THE MIN FROM EACH YEAR IN ENGLAND IS:\n {england.groupby('year').average_price.min()}")

##MIN AND MAX RECORDED NO OF CRIMES RECORDED PER AREA
print(f"THE MAX NO OF CRIMES IN EACH AREA IS:\n{data.groupby('area').no_of_crimes.max().sort_values(ascending=True)}")
print(f"\nTHE MIN NO OF CRIMES IN EACH AREA IS:\n{data.groupby('area').no_of_crimes.min().sort_values(ascending=False)}")

##SHOW THE TOTAL COUNTS OF RECORDS WHERE AVERAGE PRICE IS LESS THAN 100000
below_100000 = data[data['average_price'] < 100000]
print(f"THE ROWS ARE:\n{below_100000}")
print(f"\nTHE NUMBER IS:{below_100000.shape[0]}")
print(f"\nIN EACH AREA:\n{below_100000.area.value_counts()}")




