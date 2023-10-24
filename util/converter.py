import pandas as pd

# Replace 'input_file.csv' with the path to your CSV file.
input_file = 'image_ids_and_rotation.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Create a new column 'Combined' by concatenating 'Subset' and 'ImageID' with '/' in between
df['Combined'] = df['Subset'] + '/' + df['ImageID']

# Save the selected data to a new CSV file without column headers
# Replace 'output_file.csv' with the desired output file name.
output_file = 'imageIDs.csv'
df[['Combined']].to_csv(output_file, index=False, header=False)
