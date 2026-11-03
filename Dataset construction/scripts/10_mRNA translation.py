import pandas as pd
from Bio.Seq import Seq

WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)

# File paths
input_csv = f'{WORK_DIR}/Yeast/Yeast_NM_filtered_CDS_cleaned3.csv'  # Replace with your input file path
output_csv = f'{WORK_DIR}/Yeast/Yeast_sequences_translated.csv'  # Replace with your output file path

# Load the CSV file
data = pd.read_csv(input_csv)

# Ensure the column with nucleotide sequences is correctly identified
# Assuming the nucleotide sequences are in the 5th column
nucleotide_column = data.columns[6]

# Translate nucleotide sequences to amino acid sequences
amino_acid_sequences = []

for nucleotide_sequence in data[nucleotide_column]:
    try:
        # Create a Seq object and translate it
        seq_obj = Seq(nucleotide_sequence)
        amino_acid_seq = seq_obj.translate(to_stop=True)  # Stop translation at the first stop codon
        amino_acid_sequences.append(str(amino_acid_seq))
    except Exception as e:
        # Handle any translation errors
        print(f"Error translating sequence: {nucleotide_sequence}. Error: {e}")
        amino_acid_sequences.append("")

# Add the new column with amino acid sequences
data['Translated AA Sequence'] = amino_acid_sequences

# Save the updated DataFrame to a new CSV file
data.to_csv(output_csv, index=False)

print(f"Data saved to {output_csv}")