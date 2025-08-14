import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



 ####### this script is for cleaning the sales dataset #########
df = pd.read_csv("sales_dashboard/data/raw/train.csv")

# Display the first few rows and info to check the data
print(df.head())
print(df.info()) # Check for missing values in the dataset
print(df.isnull().sum())

#check the Customer ID column
print(df['Customer ID'].unique())

#check the Segment column
print(df['Segment'].unique())

# check the Category column
print(df['Category'].unique())
# check the Sub-Category column
print(df['Sub-Category'].unique())

# check the postal code column
print(df['Postal Code'].unique())

# print the nan values in the dataset
print(df[df.isna().any(axis=1)])

# convert 'Order Date' and 'Ship Date' to datetime format   

# first, we need to clean the 'Order Date' and 'Ship Date' columns
date_cols = ["Order Date", "Ship Date"]

for c in date_cols:
    raw = df[c].astype(str)

    raw = (raw.str.replace('\u200b', '', regex=False) 
              .str.replace('\xa0', ' ', regex=False)   
              .str.strip()
              .replace({'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA}))

    d = pd.to_datetime(raw, format='%m/%d/%Y', errors='coerce')
    print(df.info())
    mask = d.isna() & raw.notna()
    d.loc[mask] = pd.to_datetime(raw[mask], dayfirst=True, errors='coerce')

    df[c + "_raw"] = raw          
    df[c] = d

for c in date_cols:
    print(f"{c}: {df[c].isna().sum()} NaT بعد التحويل من أصل {len(df)} صف")
    
print(df.columns)
