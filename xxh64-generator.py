import os
import xxhash
import json
from tqdm import tqdm

def generate_checksums(directory, max_memory_usage):
    checksums = {}
    total_memory_usage = 0
    for root, _, files in os.walk(directory):
        for file in tqdm(files, desc="Hashing files", unit="file"):
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                hash_obj = xxhash.xxh64()
                while True:
                    # Calculate an optimal chunk size based on available memory
                    chunk_size = max_memory_usage // 2
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
                    total_memory_usage += len(chunk)
                checksum = hash_obj.hexdigest()
            relative_path = os.path.relpath(file_path, directory)
            checksums[relative_path] = checksum
    return checksums

if __name__ == "__main__":
    directory_a = input('Path A: ')
    directory_b = input('Path B: ')
    
    # Determine an optimal chunk size to limit memory usage to 20GB
    max_memory_usage = 20 * 1024 * 1024 * 1024  # 20GB
    
    checksums_a = generate_checksums(directory_a, max_memory_usage)
    checksums_b = generate_checksums(directory_b, max_memory_usage)
    
    # Compare checksums
    successful_comparison = True
    failed_files = {}
    for file_path, checksum in checksums_a.items():
        if file_path in checksums_b:
            if checksums_b[file_path] != checksum:
                successful_comparison = False
                failed_files[file_path] = {
                    "checksum_a": checksum,
                    "checksum_b": checksums_b[file_path]
                }
        else:
            successful_comparison = False
            failed_files[file_path] = {
                "checksum_a": checksum,
                "checksum_b": None  # File not found in B
            }
    
    # Output full lists of A and B hashes
    full_hashes_output = {
        "checksums_a": checksums_a,
        "checksums_b": checksums_b
    }
    
    json_file_path = os.path.join(directory_b, "checksum_comparison.json")
    with open(json_file_path, "w") as json_file:
        json.dump(full_hashes_output, json_file, indent=4)
    
    if successful_comparison:
        print("Checksum comparison was successful. All files match.")
    else:
        print("Checksum comparison was not successful. Failed checksums saved to:", json_file_path)
