import requests
import pandas as pd
from tqdm import tqdm

def get_refseq_id(uniprot_id):
    """
    Fetch the RefSeq NM ID for a given UniProt ID by searching for terms starting with NM_.
    """
    base_url = f"https://www.uniprot.org/uniprotkb/{uniprot_id}.json"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()

        data_str = str(data)
        start_index = data_str.find("NM_")
        if start_index != -1:
            end_index = data_str.find("'", start_index)
            nm_id = data_str[start_index:end_index]
            return nm_id

        return "RefSeq NM ID not found."

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def process_csv(input_file, output_file):
    """
    Process the CSV file to add RefSeq NM IDs corresponding to UniProt IDs.
    Adds a tqdm progress bar.
    """
    df = pd.read_csv(input_file)

    # Initialize tqdm progress bar
    tqdm.pandas(desc="Fetching NM IDs")

    # Apply function with progress bar
    df['NM_ID'] = df.iloc[:, 0].progress_apply(get_refseq_id)

    df.to_csv(output_file, index=False)
    print(f"\n✅ Updated CSV saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = '/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_gene_names.csv'
    output_file = '/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_NM.csv'
    process_csv(input_file, output_file)
