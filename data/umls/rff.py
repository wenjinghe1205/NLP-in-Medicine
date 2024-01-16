import pandas as pd

# Adjust the path to your file
file_path = '/Users/jianli/Desktop/MA Program/3rd semester/NLP in Medicine/UMLS2023/META/MRCONSO.RRF'

# Define the columns based on the MRCONSO.RRF format
columns = ['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 'SUPPRESS', 'CVF']
# Read the file using the appropriate separator and column names


try:
    # Read the file
    df = pd.read_csv(file_path, sep='|', names=columns, engine='python', quotechar='"', error_bad_lines=False, index_col=False)

    # Filter for English language records
    df_english = df[df['LAT'] == 'ENG']

    # Check if the filtered DataFrame is empty
    if df_english.empty:
        print("No English records found.")
    else:
        # Define the output file path
        output_file = '/Users/jianli/Desktop/MA Program/3rd semester/NLP in Medicine/MRCONSO_ENGLISH_ONLY.RRF'
        
        # Save the English records to a new file in RRF format
        df_english.to_csv(output_file, sep='|' or '||', index=False, header=False)
        print(f"File saved as {output_file}")

except Exception as e:
    print(f"Error reading file: {e}")
