from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import os
import time
import pandas as pd
from Bio.PDB import PDBParser, DSSP, ShrakeRupley, PPBuilder

# Reference SASA values (Miller et al. 1987)
REFERENCE_SASA = {
    'A': 113.0, 'R': 241.0, 'N': 158.0, 'D': 151.0, 'C': 140.0,
    'Q': 189.0, 'E': 183.0, 'G': 85.0, 'H': 194.0, 'I': 182.0,
    'L': 180.0, 'K': 211.0, 'M': 204.0, 'F': 218.0, 'P': 143.0,
    'S': 122.0, 'T': 146.0, 'W': 259.0, 'Y': 229.0, 'V': 160.0
}

def calculate_sasa_rsa(pdb_filename):
    try:
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('protein', pdb_filename)
        model = structure[0]

        ppb = PPBuilder()
        sequence = ''.join([str(pp.get_sequence()) for pp in ppb.build_peptides(structure)])

        dssp = DSSP(model, pdb_filename)

        sr = ShrakeRupley()
        sr.compute(structure, level="S")

        sasa_values = []
        rsa_values = []
        idx = 0
        for residue in model.get_residues():
            if residue.id[0] != ' ':
                continue
            sasa = sum(atom.sasa for atom in residue if hasattr(atom, 'sasa'))
            sasa_values.append(sasa)

            if idx < len(sequence):
                aa = sequence[idx]
                ref_sasa = REFERENCE_SASA.get(aa, 100.0)
                rsa = (sasa / ref_sasa) * 100
                rsa_values.append(rsa)
            else:
                rsa_values.append(0.0)
            idx += 1

        return pdb_filename, sasa_values, rsa_values

    except Exception as e:
        print(f"Error in {pdb_filename}: {e}")
        return pdb_filename, [], []

def process_batch(pdb_files_batch):
    results = []
    with ProcessPoolExecutor() as executor:
        for result in tqdm(executor.map(calculate_sasa_rsa, pdb_files_batch),
                           total=len(pdb_files_batch), desc="Batch: Calculating SASA & RSA"):
            results.append(result)
    return results

if __name__ == "__main__":
    # File paths
    csv_file_path = '/Users/jagjotarora/Documents/RSA project/Arabidopsis/Arabidopsis_speeds+ranks.csv'
    output_csv_file_path = '/Users/jagjotarora/Documents/RSA project/Arabidopsis/Arabidopsis_final.csv'
    pdb_folder_path = '/Users/jagjotarora/Documents/RSA project/Arabidopsis/Arabidopsis_alphafold_pdb_files'

    df = pd.read_csv(csv_file_path)
    pdb_files = [os.path.join(pdb_folder_path, f"{row[0]}.pdb") for _, row in df.iterrows()]

    batch_size = 200
    all_results = []

    for i in range(0, len(pdb_files), batch_size):
        batch = pdb_files[i:i + batch_size]
        print(f"\n🔁 Processing batch {i // batch_size + 1} of {len(pdb_files) // batch_size + 1}")
        batch_results = process_batch(batch)
        all_results.extend(batch_results)

        if i + batch_size < len(pdb_files):
            print("⏳ Cooling down for 5 minutes...")
            time.sleep(180)  # Sleep for 5 minutes

    # Combine with DataFrame
    df['SASA Profile'] = [res[1] for res in all_results]
    df['RSA Profile'] = [res[2] for res in all_results]

    df.to_csv(output_csv_file_path, index=False)
    print(f"\n✅ Updated file saved to: {output_csv_file_path}")
