import pandas as pd

# Read the first 100 rows from the CSV
input_file = "files/medium_articles.csv"  # Replace with the name of your input file
output_file = "articles_sample.csv"  # Replace with the name of your output file

# Use pandas to read the CSV and limit rows
data = pd.read_csv(input_file, nrows=100)

# Save the extracted rows to a new CSV
data.to_csv(output_file, index=False)

print(f"First 100 lines from '{input_file}' have been saved to '{output_file}'.")
