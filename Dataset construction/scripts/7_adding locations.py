import csv


def process_csv(file1, file2, output_file):
    # Read first CSV file and extract gene names
    with open(file1, 'r', newline='') as f1:
        reader1 = csv.reader(f1)
        header1 = next(reader1)  # Read header
        data1 = [row for row in reader1]  # Read all rows

    # Read second CSV file and store data in a list
    with open(file2, 'r', newline='') as f2:
        reader2 = csv.reader(f2)
        header2 = next(reader2)  # Read header
        data2 = [row for row in reader2]  # Read all rows

    output_data = []

    for row1 in data1:
        gene_name = row1[4]  # Extract gene name from second column of file1

        # Find matching rows in file2 (column index 8 for gene name, as index starts from 0)
        matching_rows = [row for row in data2 if row[8] == gene_name]

        if len(matching_rows) >= 5:
            # Search for row with 'exon' in column 3
            exon_row = next((row for row in matching_rows if 'exon' in row[2].lower()), None)

            if exon_row:
                col4_value = exon_row[3]  # Column 4
                col5_value = exon_row[4]  # Column 5
                col7_value = exon_row[6]  # Column 7 (sign)

                # Append data to output list
                output_data.append(row1 + [col4_value, col5_value, col7_value])

    # Write to output CSV file
    with open(output_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header1 + ['transcript_CDS_start', 'transcript_CDS_end', 'orientation'])  # Write new header
        writer.writerows(output_data)

    print(f"Processing complete. Results saved to {output_file}")


# Example usage
WORK_DIR = "Dataset construction/work"  # local, untracked working directory for this organism's intermediate files (see README)
#file 1: our main csv with gene names
#file 2: GTF csv file
#file 3: output main file having gene locations
process_csv(f'{WORK_DIR}/E.coli/alphafold_proteins_gene_names.csv',
            f'{WORK_DIR}/E.coli/E.coli_GTF_data.csv',
            f'{WORK_DIR}/E.coli/E.coli_gene_names+locations.csv')
