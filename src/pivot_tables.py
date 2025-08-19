import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# load the cleaned sales data
df = pd.read_csv("data/processed/sales_data_cleaned.csv")

# monthly sales pivot table
monthly = (df
   .assign(OrderMonth=pd.to_datetime(df["Order Date"]).dt.to_period("M").astype(str))
   .groupby("OrderMonth", as_index=False)["Sales"].sum()
)
plt.figure(figsize=(10,4))
sns.lineplot(data=monthly, x="OrderMonth", y="Sales", marker="o")
plt.xticks(rotation=45); plt.title("Monthly Sales Trend")
plt.tight_layout(); plt.savefig("figures/monthly_sales_trend.png")
plt.close()
monthly.to_csv("data/processed/monthly_sales.csv", index=False)

# top 10 products by sales
top_products = (df.groupby("Product Name")["Sales"]
                  .sum().nlargest(10).reset_index())
plt.figure(figsize=(10,6))
sns.barplot(data=top_products, y="Product Name", x="Sales", orient="h")
plt.title("Top 10 Products by Sales"); plt.tight_layout()
plt.savefig("figures/top_products.png"); plt.close()
top_products.to_csv("data/processed/top_products.csv", index=False)


# Days to Ship Pivot Table
days_to_ship = (
    df.assign(
        ShipDays=(pd.to_datetime(df["Ship Date"]) - pd.to_datetime(df["Order Date"])).dt.days
    )
    .groupby("Ship Mode")["ShipDays"]
    .mean()
    .reset_index()
    .sort_values(by="ShipDays")  
)

plt.figure(figsize=(8,5))
ax = sns.barplot(
    data=days_to_ship,
    x="Ship Mode",
    y="ShipDays",
    palette="viridis"
)

for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}",
                (p.get_x() + p.get_width() / 2, p.get_height()),
                ha="center", va="bottom", fontsize=10)

plt.title("Average Days to Ship by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figures/average_days_to_ship.png")
plt.close()

days_to_ship.to_csv("data/processed/average_days_to_ship.csv", index=False)

# Sales by Category Pivot Table
sales_by_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)
sales_by_category.to_csv("data/processed/sales_by_category.csv", index=False)

# sales by sub-category pivot table
sales_by_subcategory = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)
sales_by_subcategory.to_csv("data/processed/sales_by_subcategory.csv", index=False)

# sales by segment pivot table
sales_by_segment = (
    df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)
sales_by_segment.to_csv("data/processed/sales_by_segment.csv", index=False)
