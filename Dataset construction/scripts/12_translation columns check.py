import pandas as pd

WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)

# Load the CSV file
df = pd.read_csv(f'{WORK_DIR}/Arabidopsis/Arabidopsis_sequence+pdb_data.csv')  # Replace with your actual filename

# Compare column 9 and column 10 (indices 8 and 9)
mismatch_rows = df[df.iloc[:, 7] != df.iloc[:, 8]]

# Print the rows where the values differ
print(mismatch_rows)

# Create a mask where column 9 == column 10
matching_mask = df.iloc[:, 7] == df.iloc[:, 8]

# Get the rows where they do match
filtered_df = df[matching_mask]

# Save the filtered DataFrame to a new CSV
filtered_df.to_csv(f'{WORK_DIR}/Arabidopsis/Arabidopsis_sequence+pdb_data_cleaned.csv', index=False)
