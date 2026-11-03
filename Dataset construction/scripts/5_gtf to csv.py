import csv

WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)

# Path to your GTF file
gtf_file = f'{WORK_DIR}/Yeast/GCF_000146045.2_R64.ncbiRefSeq.gtf'
output_file = f"{WORK_DIR}/Yeast/Yeast_GTF_data.csv"

# Open the GTF file
with open(gtf_file, "r") as infile:
    reader = infile.readlines()

# List to store rows for the CSV
csv_data = []

# Parse each line in the GTF file
for line in reader:
    if line.strip() == "":  # Skip empty lines
        continue

    # Split the line into tab-delimited parts
    fields = line.strip().split("\t")

    # Extract the key-value pairs from the 9th column
    key_value_data = fields[8]
    key_value_pairs = key_value_data.split(";")

    # Clean and store key-value pairs
    key_value_dict = {}
    for pair in key_value_pairs:
        pair = pair.strip()
        if pair:
            try:
                # Split the key-value pair and remove any quotes
                key, value = pair.split(" ", 1)
                key_value_dict[key.strip()] = value.strip().strip('"')
            except ValueError:
                pass  # Skip if there's an issue splitting a key-value pair

    # Combine the tab-delimited data (first 8 columns) and key-value pairs
    row = fields[:8]  # First 8 columns are tab-delimited

    # Add key-value data to the row, ensuring we don't add keys as column names
    row.append(key_value_dict.get("gene_id", ""))
    row.append(key_value_dict.get("transcript_id", ""))
    row.append(key_value_dict.get("gene_name", ""))
    row.append(key_value_dict.get("exon_number", ""))
    row.append(key_value_dict.get("exon_id", ""))

    # Append the row to the CSV data list
    csv_data.append(row)

# Write the CSV data to a new CSV file
with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)

    # Writing headers: numbers 1, 2, 3, 4, etc.
    headers = [str(i) for i in range(1, len(csv_data[0]) + 1)]
    writer.writerow(headers)

    # Writing rows
    writer.writerows(csv_data)

print(f"Conversion complete. Data saved to {output_file}")
