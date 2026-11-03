import os
import time
import pandas as pd
from tqdm import tqdm
from Bio.PDB import PDBParser, DSSP
from concurrent.futures import ProcessPoolExecutor

def extract_structure_info_parallel(pdb_filename):
    try:
        parser = PDBParser()
        structure = parser.get_structure('protein', pdb_filename)
        model = structure[0]
        dssp = DSSP(model, pdb_filename)

        amino_acids = ''.join(dssp[key][1] for key in dssp.keys())
        secondary_structure = ''.join(dssp[key][2] for key in dssp.keys())

        return pdb_filename, amino_acids, secondary_structure
    except Exception as e:
        print(f"Error processing {pdb_filename}: {e}")
        return pdb_filename, '', ''

def process_batch(pdb_files_batch):
    results = []
    with ProcessPoolExecutor() as executor:
        for result in tqdm(executor.map(extract_structure_info_parallel, pdb_files_batch),
                           total=len(pdb_files_batch),
                           desc="Processing Batch"):
            results.append(result)
    return results

if __name__ == "__main__":
    # File paths
    WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)
    csv_file_path = f'{WORK_DIR}/Arabidopsis/Arabidopsis_sequences_translated.csv'
    output_csv_file_path = f'{WORK_DIR}/Arabidopsis/Arabidopsis_sequence+pdb_data.csv'
    pdb_folder_path = f'{WORK_DIR}/Arabidopsis/Arabidopsis_alphafold_pdb_files'

    # Load CSV file
    mrna_data = pd.read_csv(csv_file_path)
    pdb_files = [os.path.join(pdb_folder_path, f"{row[0]}.pdb") for _, row in mrna_data.iterrows()]

    batch_size = 200
    all_results = []

    for i in range(0, len(pdb_files), batch_size):
        batch = pdb_files[i:i + batch_size]
        print(f"\n🔁 Processing batch {i // batch_size + 1} of {len(pdb_files) // batch_size + 1}")
        batch_results = process_batch(batch)
        all_results.extend(batch_results)

        if i + batch_size < len(pdb_files):
            print("⏳ Cooling down for 5 minutes...")
            time.sleep(240)  # 5 minutes

    # Combine with original data
    mrna_data['Extracted AA Sequence'] = [res[1] for res in all_results]
    mrna_data['Secondary Structure Profile'] = [res[2] for res in all_results]

    # Save to CSV
    mrna_data.to_csv(output_csv_file_path, index=False)
    print(f"\n✅ Data saved to {output_csv_file_path}")
