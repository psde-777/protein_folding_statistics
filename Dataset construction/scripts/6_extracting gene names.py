import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time

# Read the UniProt IDs from CSV
df = pd.read_csv('/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_extracted_filtered.csv')

# Print column names to ensure correct naming (just for debugging)
print("CSV Loaded, Columns:", df.columns)

# Clean column names by stripping any leading/trailing spaces
df.columns = df.columns.str.strip()

# Print a message indicating that column names were cleaned
print("Column names cleaned.")


# Function to get gene name for a UniProt ID
def get_gene_name(uniprot_id):
    print(f"Fetching gene name for UniProt ID: {uniprot_id}")  # Show progress for each ID
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"

    retries = 3  # Number of retries if request fails
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # Set a 10-second timeout for each request
            if response.status_code == 200:
                print(f"Success: Data received for {uniprot_id}. Parsing XML...")
                # Parse the XML response using ElementTree
                tree = ET.ElementTree(ET.fromstring(response.content))
                root = tree.getroot()

                # Extract gene names using XPath-like search
                gene_names = [gene.text for gene in
                              root.findall('.//{http://uniprot.org/uniprot}gene/{http://uniprot.org/uniprot}name')]

                if gene_names:
                    print(f"Gene name found: {gene_names[0]}")  # Print the gene name found
                    return gene_names[0]  # Return the first gene name
                else:
                    print(f"No gene name found for {uniprot_id}")
                    return None
            else:
                print(f"Failed to fetch data for {uniprot_id}, Status Code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {uniprot_id} (Attempt {attempt + 1}/{retries}): {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
    print(f"Giving up on {uniprot_id} after {retries} attempts.")
    return None


# Apply the function to the DataFrame
print("Starting gene name retrieval process...")
df['gene_name'] = df['uniprotAccession'].apply(get_gene_name)

# Save the result to a new CSV
df.to_csv('/Users/jagjotarora/Documents/RSA project/Yeast/Yeast_alphafold_proteins_gene_names.csv', index=False)
print("Gene names fetched and saved to 'uniprot_with_gene_names.csv'")
