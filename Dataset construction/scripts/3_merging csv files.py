import pandas as pd

# Load the first CSV file
file1_path = '/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_pdb_files/proteins.csv'
file1_df = pd.read_csv(file1_path)

# Load the second CSV file
file2_path = '/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_pdb_files/proteins_2.csv'
file2_df = pd.read_csv(file2_path)
'''
file3_path = '/Users/jagjotarora/Documents/RSA project/Arabidopsis/Arabidopsis_alphafold_pdb_files/proteins_3.csv'  # Replace with your actual second file path
file3_df = pd.read_csv(file3_path)

file4_path = '/Users/jagjotarora/Documents/RSA project/Arabidopsis/Arabidopsis_alphafold_pdb_files/proteins_4.csv'  # Replace with your actual second file path
file4_df = pd.read_csv(file4_path)
'''
# Merge the two DataFrames
combined_df = pd.concat([file1_df, file2_df], ignore_index=True)

# Save the sorted merged DataFrame to a new CSV file
output_file_path = '/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_extracted.csv'
combined_df.to_csv(output_file_path, index=False)

print(f"file saved at {output_file_path}")
