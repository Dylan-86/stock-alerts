#%%
import pandas as pd

def sort_csv(input_file, output_file, sort_column='stock'):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Sort the DataFrame by the specified column in alphabetical order
    df_sorted = df.sort_values(by=sort_column, ascending=True)

    # Save the sorted DataFrame to the specified output file
    df_sorted.to_csv(output_file, index=False)

    print(f"CSV file sorted by column '{sort_column}' and saved as '{output_file}'.")
