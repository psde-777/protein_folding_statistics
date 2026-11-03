import ssl
import pandas as pd
from Bio import Entrez, SeqIO
import time

def print_cds_sequence(ncbi_id, email="jagjotarora07@gmail.com"):
    Entrez.email = email
    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        # Start the timer to track the retrieval time
        start_time = time.time()

        # Fetch the GenBank record for the given NM ID
        handle = Entrez.efetch(db="nuccore", id=ncbi_id, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()

        # Extract CDS sequence
        for feature in record.features:
            if feature.type == "CDS":
                cds_seq = feature.extract(record.seq)
                elapsed_time = time.time() - start_time
                if elapsed_time > 30:
                    print(f"Retrieval for {ncbi_id} took more than 30 seconds, skipping.")
                    return None
                return str(cds_seq)

        # If no CDS is found, print and return None
        print(f"No CDS found for {ncbi_id}")
        return None

    except Exception as e:
        print(f"Error fetching CDS for {ncbi_id}: {e}")
        return None

def process_csv_with_cds(input_csv, output_csv, id_column="NM_ID"):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv)

    # List to keep track of rows that will be added to the output file
    valid_rows = []

    for index, row in df.iterrows():
        nm_id = row[id_column]
        print(f"Fetching CDS for NM ID: {nm_id}...")

        # Get the CDS sequence
        cds_sequence = print_cds_sequence(nm_id)

        # If sequence is valid (not None), add the row to valid_rows
        if cds_sequence:
            row['Retrieved_sequence'] = cds_sequence
            valid_rows.append(row)
        else:
            print(f"Skipping {nm_id} due to errors or timeout.")

    # Create a new DataFrame with valid rows
    valid_df = pd.DataFrame(valid_rows)

    # Save the new DataFrame to a CSV file
    valid_df.to_csv(output_csv, index=False)
    print(f"\n✅ Output saved to: {output_csv}")

# Example usage
if __name__ == "__main__":
    WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)
    input_file = f'{WORK_DIR}/Yeast/Yeast_NM_filtered.csv'  # Replace with your input CSV file path
    output_file = f'{WORK_DIR}/Yeast/Yeast_NM_filtered_CDS.csv'  # Replace with your output CSV file path
    process_csv_with_cds(input_file, output_file)
