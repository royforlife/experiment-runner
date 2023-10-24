import os
import glob
import pandas as pd

# Define the base directory pattern
base_directory_pattern = "~/green-lab/experiment-runner/examples/powerjoular-compress/experiments/huffman_formal*"

# Define the columns you want to extract
desired_columns = ["compression_ratio", "compression_time", "saving_size", "total_power", "cpu_utilization", "energy_efficiency"]

# Create an empty DataFrame to store the results
result_df = pd.DataFrame(columns = ["algo-format-size-repetation","compression_ratio", "compression_time", "saving_size", "total_power", "cpu_utilization", "energy_efficiency"])

# Use glob to find directories matching the pattern
matching_directories = glob.glob(os.path.expanduser(base_directory_pattern))

# Iterate through the matching directories
for base_directory in matching_directories:
    # Extract the date-time portion from the directory name
    directory_name = os.path.basename(base_directory)

    # Iterate through the directories
    # for root, dirs, files in os.walk(base_directory):
    dirs = []
    for num in range(1200):
        dirs.append(f"run_{num}")
    root=base_directory
    for dir_name in dirs:
        # Check if the directory name starts with "run_"
        if dir_name.startswith("run_"):
            # list all the files in the directory
            files = os.listdir(os.path.join(root, dir_name))
            if len(files) == 1:
                filename = files[0]
                csv_file_path = os.path.join(root, dir_name, filename)
                # Check if the CSV file exists in the directory
                if os.path.exists(csv_file_path):
                    # Get the file name without extension
                    file_name = os.path.splitext(os.path.basename(csv_file_path))[0]

                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(csv_file_path, sep=',', header=0)

                    # Extract the desired columns
                    # check if the desired columns exist in the DataFrame
                    if not set(desired_columns).issubset(df.columns):
                        print(f"Skipping {file_name} because it doesn't have all the desired columns")
                        continue
                    # df["algo-format-size-repetation"] = f"huffman-{file_name}"
                    # columns = desired_columns.append("algo-format-size-repetation")
                    # make algo-format-size-repetation be the first column
                    # check df is not empty
                    if df.empty:
                        print(f"Skipping {file_name} because it is empty")
                        continue
                    extracted_data = df[desired_columns]
                    extracted_data["algo-format-size-repetation"] = f"huffman-{file_name}"
                    # make algo-format-size-repetation be the first column
                    # get second row
                    # check extracted_data.shape[0] > 1
                    if extracted_data.shape[0] <= 1:
                        print(f"Skipping {file_name} because it has less than 2 rows")
                        continue
                    extracted_data = extracted_data.iloc[1]
                    print(extracted_data)
                    # Add the file name as the first column
                    # extracted_data.insert(0, "algo-format-size-repetation", file_name)

                    # Append the data2 to the result DataFrame
                    # import pdb; pdb.set_trace()
                    result_df = result_df.append(extracted_data, ignore_index=True)

# Display the resulting DataFrame
print(result_df)
# Write the DataFrame to a CSV file
result_df.to_csv("output_result_huffman_all.csv", index=True)
# import pdb; pdb.set_trace()
