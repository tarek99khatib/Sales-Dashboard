import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# load the cleaned sales data
df = pd.read_csv("data/processed/sales_data_cleaned.csv")

# Display the first few rows and info to check the data
print(df.head())

# discover the basic information about the dataset
print(df.info())  # Check for missing values in the dataset
print(df.isnull().sum())
print(df.describe())
print(df.shape)

####----- EDA on the sales dataset -----####

## sales distribution
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
sns.histplot(df["Sales"], bins=50, kde=True, ax=axes[0])
axes[0].set_title("Sales Distribution")


sns.boxplot(x=df["Sales"], ax=axes[1])
axes[1].set_title("Sales Boxplot")

sns.histplot(df[df["Sales"] < 5000]["Sales"], bins=30, kde=True, ax=axes[2])
axes[2].set_title("Sales Distribution (Zoomed In)")
plt.tight_layout()
plt.savefig("figures/sales_distribution.png")
plt.close()

## sales by category and sub-category analysis
categories = df["Category"].unique()
palette = dict(zip(categories, sns.color_palette("Set2", n_colors=len(categories))))

# Sales by Category
plt.figure(figsize=(8,5))
sns.barplot(
    data= df,
    x="Category",
    y="Sales",
    hue="Category",
    estimator=sum,
    order= df.groupby("Category")["Sales"].sum().sort_values(ascending=False).index,
    palette=palette
    )
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.savefig("figures/sales_by_category.png")
plt.close()

# Sales by Sub-Category with colors by Category
plt.figure(figsize=(12,6))
sns.barplot(
    data=df,
    x="Sub-Category",
    y="Sales",
    hue="Category",
    estimator=sum,
    order=df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False).index,
    palette=palette
)
plt.title("Total Sales by Sub-Category (Colored by Category)")
plt.xlabel("Sub-Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("figures/sales_by_subcategory.png")
plt.close()

## Sales by city
plt.figure(figsize=(12,6))
sns.barplot(
    data=df,
    x="City",
    y="Sales",
    hue="Category",
    estimator=sum,
    order=df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(10).index,
    palette=palette
)
plt.title("Total Sales by City (Top 10 Cities)")
plt.xticks(rotation=45)
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("figures/sales_by_city.png")
plt.close()

## Sales by State
plt.figure(figsize=(12,6))
sns.barplot(
    data=df,
    x="State",
    y="Sales",
    hue="Category",
    estimator=sum,
    order=df.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10).index,
    palette=palette
)
plt.title("Total Sales by State (Top 10 States)")
plt.xticks(rotation=45)
plt.xlabel("State")
plt.ylabel("Total Sales")
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("figures/sales_by_state.png")
plt.close()

## Sales by Region
plt.figure(figsize=(12,6))
sns.barplot(
    data=df,
    x="Region",
    y="Sales",
    hue="Category",
    estimator=sum,
    order=df.groupby("Region")["Sales"].sum().sort_values(ascending=False).index,
    palette=palette
)
plt.title("Total Sales by Region")
plt.xticks(rotation=45)
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("figures/sales_by_region.png")
plt.close()

## Sales by Ship Mode
ship_sales = df.groupby("Ship Mode")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,5))
color_palette = sns.color_palette("Set2", n_colors=len(ship_sales))
plt.pie(
    ship_sales,
    labels=ship_sales.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=color_palette,
)
plt.title("Sales Distribution by Ship Mode")
plt.tight_layout()
plt.savefig("figures/sales_by_ship_mode.png")
plt.close()


print(df["Postal Code"].unique())
