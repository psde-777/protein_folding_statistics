import pandas as pd

def remove_invalid_nm_rows(input_csv, output_csv):
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Identify the last column name
    last_column = df.columns[-1]

    # Filter out rows where the last column has "RefSeq NM ID not found"
    df_filtered = df[df[last_column] != "RefSeq NM ID not found."]

    # Save the cleaned DataFrame to a new CSV
    df_filtered.to_csv(output_csv, index=False)
    print(f"✅ Filtered CSV saved to: {output_csv}")

# Example usage:
WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)
input_csv_path = f"{WORK_DIR}/Yeast/Yeast_NM.csv"
output_csv_path = f"{WORK_DIR}/Yeast/Yeast_NM_filtered.csv"
remove_invalid_nm_rows(input_csv_path, output_csv_path)
