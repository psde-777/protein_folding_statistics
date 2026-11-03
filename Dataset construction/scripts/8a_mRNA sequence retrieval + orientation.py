import csv
from Bio import SeqIO


def extract_sequence(fasta_file, start, stop):
    """
    Extracts a sequence from a FASTA file given the start and stop positions.

    :param fasta_file: Path to the FASTA file.
    :param start: Start position (1-based index).
    :param stop: Stop position (1-based index).
    :return: Extracted sequence as a string.
    """
    with open(fasta_file, "r") as file:
        for record in SeqIO.parse(file, "fasta"):
            sequence = record.seq
            return str(sequence[start - 1:stop])  # Convert to 0-based index
    return None


def process_csv(input_csv, output_csv, fasta_file):
    """
    Reads an input CSV, extracts sequences based on start and stop positions if column 5 contains '+',
    and writes a new CSV with the extracted sequences.

    :param input_csv: Path to the input CSV file.
    :param output_csv: Path to the output CSV file.
    :param fasta_file: Path to the FASTA file.
    """
    with open(input_csv, "r") as infile, open(output_csv, "w", newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)
        header.append("Retrieved_Sequence")
        writer.writerow(header)

        total_rows = sum(1 for row in open(input_csv)) - 1
        infile.seek(0)
        next(reader)  # Skip header
        processed_count = 0

        for i, row in enumerate(reader, 1):
            if row[7] == "-":  # Column 5 (zero-based index: 4) should be '+' to process
                continue

            try:
                start = int(row[5])  # Column 3 (zero-based index: 2)
                stop = int(row[6])  # Column 4 (zero-based index: 3)
                sequence = extract_sequence(fasta_file, start, stop)
                row.append(sequence if sequence else "Error")
            except Exception as e:
                row.append(f"Error: {e}")

            writer.writerow(row)
            processed_count += 1
            print(f"Processed {processed_count} rows", end="\r")

# Example usage
fasta_path = "/Users/jagjotarora/Documents/RSA project/E.coli/E.coli_whole_genome.fasta"  # Replace with actual FASTA file path
input_csv_path = "/Users/jagjotarora/Documents/RSA project/E.coli/E.coli_gene_names+locations.csv"  # Replace with actual input CSV file path
output_csv_path = "/Users/jagjotarora/Documents/RSA project/E.coli/E.coli_sequences(+).csv"  # Replace with desired output CSV file path

process_csv(input_csv_path, output_csv_path, fasta_path)
print("\nProcessing complete!")