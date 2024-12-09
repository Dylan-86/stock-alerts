#%%
import pandas as pd

# Load the CSV file
input_file = 'stocks.csv'
output_file = 'stocks.csv'

# Define the column name or index to sort by (change 'ColumnName' to the appropriate column header)
sort_column = 'stock'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Sort the DataFrame by the specified column in alphabetical order
df_sorted = df.sort_values(by=sort_column, ascending=True)

# Save the sorted DataFrame to a new CSV file
df_sorted.to_csv(output_file, index=False)

print(f"CSV file sorted by column '{sort_column}' and saved as '{output_file}'.")
