import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import colormaps

df = pd.read_csv(r"C:\\Users\\62704\\Documents\\GitHub\\intro-to-ds-24-25-Yinshu_Lu\\data\\Video_Games_Sales_as_at_22_Dec_2016.csv")
df

df = df.dropna()

#unique labels
df["Genre"].unique()

#Game genre distribution
df["Genre"].value_counts()

#Using np.floor() to round all the values to nearest integer
Global_Sales = np.floor(df["Global_Sales"].values)

fig, ax = plt.subplots(figsize=(12,8)) 
number_of_bins = 25
#Plot histogram
h = ax.hist(Global_Sales, bins=number_of_bins)
ax.set_ylabel("Number of games")
ax.set_xlabel("Global_Sales (millions)")
ax.set_title("Distribution of game sales")

#Mean
mean = df["Global_Sales"].mean()
print(mean)

#Mode
mode = df["Global_Sales"].mode()
print(mode)

#Median
median = df["Global_Sales"].median()
print(median)

# Three most common items
top_3 = Counter(Global_Sales).most_common(3)
print(top_3)

labels = df["Genre"].unique()
np.linspace(0,1,len(labels))

#Colour map gives use a continuous range of colours
colors = colormaps['tab20']
#List comprehension gets 10 colours from the colour map between 0 and 1 (e.g. 0, 0.1, 0.2, 0.3....)
colors_list = [colors(i) for i in np.linspace(0,1,len(labels))]
colors_dict = {labels[i]:colors_list[i] for i in range(len(labels))}

#Group statistics by game type
grouped = df.groupby("Genre")
mean_by_genre = grouped["Global_Sales"].mean().sort_values()
median_by_genre = grouped["Global_Sales"].median()
print(mean_by_genre)

fig, ax = plt.subplots(figsize=(12,6))
mean_by_genre.plot(kind="bar", ax=ax, color=colors_list)
ax.set_title("Average global sales by genre")
ax.set_ylabel("Sales (millions)")

rows = 3
cols = 4
fig, ax = plt.subplots(rows, cols, figsize=(15, 12))

x_min = 0
x_max = df["Global_Sales"].quantile(0.99)

for i, label in enumerate(labels):
    Global_Sales = df[df["Genre"]==label]["Global_Sales"].values
    col = i%cols
    row = int(np.floor(i/cols))
    axis = ax[row,col]
    axis.plot(Global_Sales,np.arange(len(Global_Sales)), "o", color=colors_list[i], ms=3)
    axis.set_title(label)
    axis.set_xlim(x_min, x_max)
    axis.set_xlabel("Global Sales (millions)")

plt.tight_layout()
plt.show()

rows = 3
cols = 4
fig, ax = plt.subplots(rows, cols, figsize=(15,12))

x_max = df["Global_Sales"].quantile(0.99) 

for i,label in enumerate(labels):
    global_sales = df[(df["Genre"] == label) & (df["Global_Sales"] < x_max)]["Global_Sales"].values
    col = i%cols
    row = int(np.floor(i/cols))
    axis = ax[row,col]
    number_of_bins = 20
    h = axis.hist(global_sales, bins=number_of_bins,color=colors_list[i])
    axis.set_title(label)
    #Set the bounds on the x axis so all graphs are comparable
    axis.set_xlim(0, x_max)
    axis.set_xlabel("Global sales (millions)")

plt.tight_layout()
plt.show()

def sales_range(x):
    return x["Global_Sales"].max() - x["Global_Sales"].min()

#Get range from grouped items
range_sales = grouped.apply(sales_range, include_groups=False).sort_values()
print(range_sales)

#Plot
sorted_colors = [colors_dict[i] for i in range_sales.index]
fig, ax = plt.subplots(figsize=(12,5))
ax.set_ylabel("sales range")
ax.bar(range_sales.index,range_sales,0.5,color =sorted_colors)
#Characters that are too long overlap
plt.xticks(rotation=45)
plt.title("Sales Range by Genre")
plt.show()

#Get standard deviation from grouped items
std_dev = grouped["Global_Sales"].std().sort_values(ascending=False)  # 按标准差降序排序

#Plot
sorted_colors = [colors_dict[i] for i in std_dev.index]
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(std_dev.index,std_dev.values,0.5,color = sorted_colors)
ax.set_ylabel("Global_sales std (millions)")

plt.tight_layout()
plt.show()

for genre in mean_by_genre.index:
    mean = mean_by_genre.loc[label]
    std = std_dev.loc[label]
    group = df[df["Genre"]==label]
    dist = np.abs(group["Global_Sales"]-mean)/std
    
    #select rows from group, set zscore coloumn
    df.loc[group.index,"zscore"] = dist
    
fig, ax = plt.subplots(figsize=(12,5))
y = df["zscore"].values
ax.set_ylabel("z score for Global_Sales")
ax.set_xlabel("all games")
ax.plot(y,"x")

plt.tight_layout()
plt.show()
