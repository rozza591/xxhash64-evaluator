import os
import xxhash
from tqdm import tqdm

def generate_checksums(directory):
    checksums = {}
    for root, _, files in os.walk(directory):
        for file in tqdm(files, desc="Hashing files", unit="file"):
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                checksum = xxhash.xxh64(f.read()).hexdigest()
            relative_path = os.path.relpath(file_path, directory)
            checksums[relative_path] = checksum
    return checksums

def compare_checksums(checksums_a, checksums_b):
    return checksums_a == checksums_b

if __name__ == "__main__":
    directory_a = input('Path A: ')
    directory_b = input('Path B: ')
    
    checksums_a = generate_checksums(directory_a)
    checksums_b = generate_checksums(directory_b)

    match = compare_checksums(checksums_a, checksums_b)

    if match:
        print("Checksums match.")
    else:
        print("Checksums do not match.")
