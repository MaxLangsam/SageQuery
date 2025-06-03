from datasets import load_dataset
import pandas as pd

# Load the dataset
dataset = load_dataset("Sharathhebbar24/sql-create-context")

# Convert to pandas DataFrame
df = pd.DataFrame(dataset['train'])

# Save to CSV
df.to_csv('sql-create-context.csv', index=False)
print("Dataset downloaded and saved as sql-create-context.csv")
