import pandas as pd
import os
import math
from concurrent.futures import ProcessPoolExecutor

def get_byte_counts(filepath):
    """
    Get the byte counts for a binary file.

    Args:
    - filepath (str): Path to the file

    Returns:
    - list: A list of counts for each byte value (0-255).
    """
    byte_counts = [0] * 256  # There are 256 possible byte values (0-255)

    with open(filepath, 'rb') as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            byte_counts[byte[0]] += 1

    return byte_counts


def compute_entropy_from_counts(byte_counts):
    """
    Compute entropy given byte counts.

    Args:
    - byte_counts (list): List of counts for each byte value.

    Returns:
    - float: entropy value.
    """
    total_bytes = sum(byte_counts)
    entropy = 0.0

    for count in byte_counts:
        if count > 0:
            p_x = count / total_bytes
            entropy += -p_x * math.log2(p_x)

    return entropy


def compute_folder_entropy(folder_path, max_workers=None):
    """
    Compute the combined information entropy of all binary files in a given folder path using parallel computation.

    Args:
    - folder_path (str): Path to the folder
    - max_workers (int, optional): Max number of processes for the pool. Default is None.

    Returns:
    - float: combined entropy value for all files under the folder.
    """
    if not os.path.exists(folder_path):
        raise ValueError(f"'{folder_path}' does not exist.")

    if not os.path.isdir(folder_path):
        raise ValueError(f"'{folder_path}' is not a directory.")

    total_byte_counts = [0] * 256
    filepaths = [os.path.join(root, file) for root, _, files in os.walk(folder_path) for file in files]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for byte_counts in executor.map(get_byte_counts, filepaths):
            total_byte_counts = [x + y for x, y in zip(total_byte_counts, byte_counts)]

    return compute_entropy_from_counts(total_byte_counts)


# Read the entropy CSV file
# entropy_df_flv = pd.read-csv('./data/entropy_flv.csv', sep=',', header=0)
# entropy_df_mp4 = pd.read-csv('./data/entropy_mp4.csv', sep=',', header=0)
# entropy_df_jpg = pd.read-csv('./data/entropy_jpg.csv', sep=',', header=0)
# entropy_df_png = pd.read-csv('./data/entropy_png.csv', sep=',', header=0)
# entropy_df_txt = pd.read-csv('./data/entropy_txt.csv', sep=',', header=0)
# entropy_df_pdf = pd.read-csv('./data/entropy_pdf.csv', sep=',', header=0)

# read ./output_result_huffman_all.csv

if __name__ == "__main__":
    result_df_huffman = pd.read_csv('./output_result_huffman_all.csv', sep=',', header=0)
    # read ./output_result_lzw_all.csv
    result_df_lzw = pd.read_csv('./output_result_lzw_all.csv', sep=',', header=0)

    # add two columns size and entropy to result_df_huffman
    result_df_huffman['size'] = 0
    result_df_huffman['entropy'] = 0
    entropy_dict = {}

    # iterate through result_df_huffman each row
    for index, row in result_df_huffman.iterrows():
        # get the file name
        file_name = row['algo-format-size-repetation']
        # get the file format
        file_format = file_name.split('-')[1]
        # get the file size
        file_size_repetaion = file_name.split('-')[2] + '-' + file_name.split('-')[3]
        number = file_name.split('-')[-1]
        data_path = f"./data/{file_format}/{file_size_repetaion}/{number}/"
        print('index: ', index, 'data_path: ',  data_path)
        # sum the size of all files in the directory data_path
        files = os.listdir(data_path)
        file_size = 0
        for file in files:
            file_size += os.path.getsize(data_path + file) / 1024
        row['size'] = file_size
        # row['entropy'] = compute_folder_entropy(data_path, max_workers=4)
        # save the size to result_df_huffman
        result_df_huffman.loc[index, 'size'] = file_size
        # result_df_huffman.loc[index, 'entropy'] = compute_folder_entropy(data_path, max_workers=16)

        if data_path not in entropy_dict:
            entropy = compute_folder_entropy(data_path, max_workers=16)
            entropy_dict[data_path] = entropy
        result_df_huffman.loc[index, 'entropy'] = entropy_dict[data_path]

    # save result_df_huffman to ./output_result_huffman_all.csv
    result_df_huffman.to_csv("output_result_huffman_all_size_entropy.csv", index=True)

    for index, row in result_df_lzw.iterrows():
        # get the file name
        file_name = row['algo-format-size-repetation']
        # get the file format
        file_format = file_name.split('-')[1]
        # get the file size
        file_size_repetaion = file_name.split('-')[2] + '-' + file_name.split('-')[3]
        number = file_name.split('-')[-1]
        data_path = f"./data/{file_format}/{file_size_repetaion}/{number}/"
        print(data_path)
        # sum the size of all files in the directory data_path
        files = os.listdir(data_path)
        file_size = 0
        for file in files:
            file_size += os.path.getsize(data_path + file) / 1024
        row['size'] = file_size
        # row['entropy'] = compute_folder_entropy(data_path, max_workers=4)
        # save the size to result_df_huffman
        result_df_lzw.loc[index, 'size'] = file_size
        # result_df_huffman.loc[index, 'entropy'] = compute_folder_entropy(data_path, max_workers=16)

        if data_path not in entropy_dict:
            entropy = compute_folder_entropy(data_path, max_workers=16)
            entropy_dict[data_path] = entropy
        result_df_lzw.loc[index, 'entropy'] = entropy_dict[data_path]

    # save result_df_huffman to ./output_result_huffman_all.csv
    result_df_lzw.to_csv("output_result_lzw_all_size_entropy.csv", index=True)

