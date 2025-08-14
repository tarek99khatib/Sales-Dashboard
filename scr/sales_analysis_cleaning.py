import pandas as pd



####### this script is for cleaning the sales dataset #########
df = pd.read_csv("data/raw/sales_data_raw.csv")

# Display the first few rows and info to check the data
print(df.head())
print(df["Postal Code"].unique())

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


# check the prduct id 
print(df['Product ID'].unique())

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
    print(f"{c}: {df[c].isna().sum()} NaT from {len(df)} rows")
    
print(df.info())
print(df.columns) # Display the columns in the dataset

# strip whitespace from string columns
cat_cols = ["Ship Mode", "Segment", "Country", "City", "State", "Region", 
            "Category", "Sub-Category", "Product Name"]

for c in cat_cols:
    df[c] = df[c].astype(str).str.strip()
    
# for the id columns, we will convert them to string
id_cols = ["Order ID", "Customer ID", "Product ID"]
for c in id_cols:
    df[c] = df[c].astype(str).str.strip()

# postal code column
df["Postal Code"] = df["Postal Code"].astype("Int64")
df.dropna(subset=["Postal Code"], inplace=True) 

# cleaning the sales column
df["Sales"] = (df["Sales"].astype(str)
                              .str.replace(r'[\$,]', '', regex=True)
                              .astype(float))

# cleaning logic based on the 'Order Date' column and 'Ship Date' column
df = df[df["Ship Date"] >= df["Order Date"]]

# delete duplicate rows
df = df.drop_duplicates()

# check the outliers in the dataset
print(df[df["Sales"] < 0])

print(df.info()) # Check the info of the cleaned dataset

df.drop(columns=["Order Date_raw", "Ship Date_raw"], inplace=True) # Drop the raw date columns

# save the cleaned dataset
df.to_csv("data/processed/sales_data_cleaned.csv", index=False)
