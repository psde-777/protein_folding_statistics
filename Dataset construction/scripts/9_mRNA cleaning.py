import pandas as pd

WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)

# File paths
input_csv = f'{WORK_DIR}/Yeast/Yeast_NM_filtered_CDS.csv'
output_csv = f'{WORK_DIR}/Yeast/Yeast_NM_filtered_CDS_cleaned4.csv'

# Load CSV
df = pd.read_csv(input_csv)

# Sequence column (index 6 = 7th column)
seq_col = df.columns[6]

# Step 1: Replace T with U
df[seq_col] = df[seq_col].str.replace('T', 'U', regex=False)

# Step 2: Change first nucleotide to A
def fix_first_nucleotide(seq):
    if isinstance(seq, str) and len(seq) > 0:
        if seq[0] != 'A':
            return 'A' + seq[1:]
    return seq

df[seq_col] = df[seq_col].apply(fix_first_nucleotide)

# Step 3: Check for AUG start codon
mask = df[seq_col].apply(
    lambda seq: isinstance(seq, str) and seq.startswith('AUG')
)

# Print IDs of removed sequences (first column)
removed_rows = df[~mask]

print("Removed sequence IDs:")
for code in removed_rows.iloc[:, 0]:
    print(code)

# Keep only sequences starting with AUG
filtered_df = df[mask].copy()

# Save final CSV
filtered_df.to_csv(output_csv, index=False)

# Summary
print(f"\nTotal sequences: {len(df)}")
print(f"Sequences removed: {len(removed_rows)}")
print(f"Sequences retained: {len(filtered_df)}")
print(f"Output saved to: {output_csv}")