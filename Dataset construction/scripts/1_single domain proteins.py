#This code takes in uniprot codes list file
#it checks for single domain proteins and if it is yes
#then those are saved as a csv file that can be used to download alphafold files

import requests
import csv

def get_uniprot_json(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for {uniprot_id}. Status code: {response.status_code}")
        return None


def extract_domain_info(uniprot_data):
    domain_info = []

    if 'features' in uniprot_data:
        for feature in uniprot_data['features']:
            if feature['type'] == 'Domain':
                domain_info.append(feature)

    return domain_info


def process_uniprot_list(input_file, output_file):
    with open(input_file, 'r') as f:
        uniprot_ids = [line.strip() for line in f.readlines()]

    single_domain_proteins = []

    for uniprot_id in uniprot_ids:
        uniprot_data = get_uniprot_json(uniprot_id)
        if uniprot_data:
            domain_info = extract_domain_info(uniprot_data)
            domain_count = len(domain_info)

            if domain_count <= 1:  # Single-domain protein
                print(f"{uniprot_id} is a single-domain protein.")
                single_domain_proteins.append([uniprot_id])
            else:
                print(f"{uniprot_id} is a multidomain protein (Domains: {domain_count}). Skipping.")

    # Save single-domain proteins to a CSV file
    if single_domain_proteins:
        with open(output_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["UNIPROT_codes"])  # Header
            csv_writer.writerows(single_domain_proteins)
        print(f"Single-domain proteins saved to {output_file}")
    else:
        print("No single-domain proteins found.")


# Example usage
input_file = "/Users/jagjotarora/Documents/RSA project/Yeast/Uniprot_protein_list_Yeast.txt"  # Input text file with UniProt IDs
output_file = "/Users/jagjotarora/Documents/RSA project/Yeast/single_domain_proteins_Yeast.csv"  # Output CSV file
process_uniprot_list(input_file, output_file)
