## DATA ANALYSIS--BOOK SALES ##

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns #data visualization library in Python used for creating attractive, informative statistical graphs.
pd.set_option("display.max_columns", None)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.width", 1000)  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY
pd.set_option("display.max_colwidth", None) ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY ## THIS WILL GIVE ALL THE COLUMNS INSTEAD OF "...."


df = pd.read_csv(r"C:\Users\Reaga\Downloads\Books_Data_Clean.csv")
print(df.head().to_string())  ### THIS IS USED SO THAT ALL THE COLUMNS COME HORIZONTALLY


print(df.head())
print(df.describe())
df=df[df["Publishing Year"]>1900]
print(df.describe())

df.isna().sum()#df.isna(): This looks at every single cell in your DataFrame. If the cell has data, it marks it as False. If the cell is completely empty (often labeled as NaN or "Not a Number"), it marks it as True.".sum()": This takes that grid of True/False values and adds them up column by column. In Python, True is equal to 1, and False is equal to 0.
df.dropna(subset=['Book Name'], inplace=True)#df.dropna()--This is the Pandas command to "drop" (delete) rows that contain "NA" (missing) values. If you ran df.dropna() completely by itself, it would aggressively delete every single row in your entire dataset that had even one blank cell in any column.
#subset=['Book Name']-- you are telling the code: "I don't care if the Author or the Price is missing, but if the Book Name is blank, delete the whole row".
#Normally, when you run a command in Pandas, it just shows you a preview of what the data would look like, but it doesn't actually alter your saved dataset. By adding inplace=True, you are telling Pandas to make this change permanent to your df variable in the computer's memory.

#to check if data is duplicated:
print(df.duplicated().sum())

#to check unique values
print(df.nunique())

## HISTOGRAM:
sns.histplot(df["Publishing Year"], bins=10, color="orange")
plt.title("DISTRIBUTION OF PUBLISHING YEAR")
plt.xlabel("PUBLISHING YEAR")
plt.ylabel("FREQUENCY")
plt.show()

df['genre'].value_counts().plot(kind="bar")#df['genre'] uses brackets because genre is a column name in your DataFrame, and brackets are how you select a column in pandas. value_counts() is then a method called on that selected column to count how many times each unique genre appears.
plt.title("NUMBER OF BOOKS IN EACH GENRE")
plt.xlabel("GENRE")
plt.ylabel("NUMBER OF BOOKS")
plt.show()

##GROUPY
df.groupby("Author")["Book_average_rating"].mean().reset_index().sort_values(by="Book_average_rating", ascending=False)#The problem is sort_values(ascending=False) is being used without telling pandas which column to sort by after reset_index(). Once you do mean().reset_index(), you have a full DataFrame, so sort_values() needs a by= argument such as the rating column.

#BOSPLOT
sns.boxplot(x="genre", y="Book_ratings_count", data=df)
plt.xlabel("Genre")
plt.ylabel("Book Rating Count")
plt.title("BOOK RATING COUNT PER GENRE")
plt.show()

#SCATTERPLOT
plt.scatter(df["sale price"], df["units sold"])
plt.xlabel("sale price")
plt.ylabel("units sold")
plt.title("sale price vs units sold")
plt.show()

counts = df["language_code"].value_counts()
plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)#autopct="%1.1f%%" shows the percentage on each slice.labels=counts.index puts the language codes on the slices.
plt.title("Language Distribution of books")
plt.ylabel("")   # removes the default y-label
plt.show()

##CALCULATING THE TOTAL REENUE FOR EACH PUBLISHER
print(df.columns)
df.groupby("Publisher ")["publisher revenue"].sum().sort_values(ascending=False)

print(df.groupby("Author_Rating")["Book_ratings_count"].mean().sort_values(ascending=False).max())

print(df.groupby("language_code").size().sort_values(ascending=False))

print(df.groupby("Author_Rating")["Book_ratings_count"].max().sort_values(ascending=False))


plt.scatter(df["Book_average_rating"],df["Book_ratings_count"])
plt.xlabel("average rating")
plt.ylabel("number of books")
plt.title("average rating vs number of books")
plt.show()

total_gross_sales_by_author=df.groupby("Author")["sale price"].sum()
print(total_gross_sales_by_author.sort_values(ascending=False).head(20).plot(kind="bar"))
plt.xlabel("Author")
plt.ylabel("total gross sale price")
plt.title("total gross sale price vs author")
plt.show()

sns.boxplot(x="Author_Rating", y="units sold", data=df)
plt.xlabel("Author Rating")
plt.ylabel("units sold")
plt.title("units sold vs author")
plt.show()

df.groupby("Publishing Year")["units sold"].sum().plot(kind="line", marker="o")
plt.xlabel("Publishing Year")
plt.ylabel("Total units sold")
plt.title("Total units sold over publishing year")
plt.show()

###Different Dataset Versions: The tutorial might be using an older or newer version of the Kaggle dataset.
# ###Datasets on Kaggle get updated frequently by their creators, so the file you downloaded might simply have fewer rows than the one the YouTuber downloaded months or years ago





