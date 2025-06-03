import pandas as pd

# Read the CSV file
df = pd.read_csv('sql-create-context.csv')

# Print the column names
print("Column names in the dataset:")
print(df.columns.tolist())

# Print first row to see the structure
print("\nFirst row of data:")
print(df.iloc[0])
