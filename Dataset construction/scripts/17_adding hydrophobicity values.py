import pandas as pd

# Kyte & Doolittle hydrophobicity scale
hydrophobicity_scale = {
    'A': 1.8,  'R': -4.5, 'N': -3.5, 'D': -3.5,
    'C': 2.5,  'Q': -3.5, 'E': -3.5, 'G': -0.4,
    'H': -3.2, 'I': 4.5,  'L': 3.8,  'K': -3.9,
    'M': 1.9,  'F': 2.8,  'P': -1.6, 'S': -0.8,
    'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

def sequence_to_hydrophobicity(seq):
    """Convert amino acid sequence to list of hydrophobicity values."""
    return [hydrophobicity_scale.get(aa, 0.0) for aa in seq]  # unknown aa -> 0.0

def main(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    # Extract sequences from column index 8
    sequences = df.iloc[:, 10]

    # Convert sequences to hydrophobicity values
    hydro_values = sequences.apply(sequence_to_hydrophobicity)

    # Add new column
    df["Hydrophobicity values"] = hydro_values

    # Save as new CSV
    df.to_csv(output_file, index=False)
    print(f"File saved as {output_file}")

if __name__ == "__main__":
    # Change these filenames as needed
    main("/Users/jagjotarora/Desktop/CCB/Main task ExpressinHost/work/Alphafold datasets/E.coli/E.coli_dataset_completed.csv",
         "/Users/jagjotarora/Desktop/CCB/Main task ExpressinHost/work/Alphafold datasets/E.coli/E.coli_dataset_hydrophobicity.csv")
