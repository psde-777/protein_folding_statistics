import pandas as pd

def save_codes_to_txt(input_csv, output_txt):
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    # Extract the first column (assuming it's the first column and contains the codes)
    codes = df.iloc[:, 0].dropna()  # Drop NaN values if any

    # Convert the list of codes to a comma-separated string
    codes_str = ','.join(codes.astype(str))

    # Write the codes to the output text file
    with open(output_txt, 'w') as f:
        f.write(codes_str)

# Example usage
input_csv = "/Users/jagjotarora/Documents/RSA project/Yeast/single_domain_proteins_Yeast.csv"  # Replace with your CSV file path
output_txt = "/Users/jagjotarora/Documents/RSA project/Yeast/single_domain_proteins_Yeast.txt"  # Replace with your desired output .txt file path
save_codes_to_txt(input_csv, output_txt)
