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

if __name__ == "__main__":
    folder = input("Enter the path to the folder: ")
    entropy = compute_folder_entropy(folder)
    print(f"Combined entropy for all files under '{folder}': {entropy:.4f}")
