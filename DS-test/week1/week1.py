import pandas as pd

df = pd.read_csv(r"C:\\Users\\62704\\Documents\\GitHub\\intro-to-ds-24-25-Yinshu_Lu\\data\\Student_Performance_on_an_Entrance_Examination.csv")
df

df.columns

df.dtypes

df.describe(include = "all")

df["Gender"].describe()

df["Gender"].value_counts()

df["Caste"].value_counts()

df[["Gender","Caste"]].value_counts()

df.sort_values(by='Performance', ascending=False)[:10]

coached_students = df[df["coaching"] != "NO"]
coached_students

df.count() / len(df)

df[df["time"].isna()]["time"].values

df[["Gender", "Caste", "Performance"]].head(10)

time = df.sort_values(by="time", ascending=True)
print(time.head(5))

df["Performance"].value_counts()

df[["Class_X_Percentage", "Class_XII_Percentage"]].isna().sum()