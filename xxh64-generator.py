import os
import xxhash
import json
from tqdm import tqdm

def generate_checksums(directory):
    checksums = {}
    for root, _, files in os.walk(directory):
        for file in tqdm(files, desc="Hashing files", unit="file"):
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                hash_obj = xxhash.xxh64()
                while True:
                    chunk = f.read(8000)  # Read and hash in 8KB chunks
                    if not chunk:
                        break
                    hash_obj.update(chunk)
                checksum = hash_obj.hexdigest()
            relative_path = os.path.relpath(file_path, directory)
            checksums[relative_path] = checksum
    return checksums

if __name__ == "__main__":
    directory_a = input('Path A: ')
    directory_b = input('Path B: ')
    
    checksums_a = generate_checksums(directory_a)
    checksums_b = generate_checksums(directory_b)
    
    # Compare checksums and save the failed ones to a JSON file
    failed_checksums = {}
    for file_path, checksum in checksums_a.items():
        if file_path in checksums_b and checksums_b[file_path] != checksum:
            failed_checksums[file_path] = {
                "checksum_a": checksum,
                "checksum_b": checksums_b[file_path]
            }
    
    json_file_path = os.path.join(directory_b, "failed_checksums.json")
    with open(json_file_path, "w") as json_file:
        json.dump(failed_checksums, json_file, indent=4)
    
    if not failed_checksums:
        print("Checksum check was successful. All files match.")
    else:
        print("Checksum check was not successful. Failed checksums saved to:", json_file_path)
