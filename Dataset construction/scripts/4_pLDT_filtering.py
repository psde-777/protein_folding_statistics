import pandas as pd

# Step 1: Read the CSV
df = pd.read_csv('/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_extracted.csv')

# Step 2: Filter rows where globalMetricValue is >= 85
filtered_df = df[df['globalMetricValue'] >= 75]

# Step 3: Save to a new CSV
filtered_df.to_csv('/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_extracted_filtered.csv', index=False)