import hashlib
import os
import json

def hash_file(filepath):
    """Function to hash a file using SHA-256."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            buf = file.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def load_existing_hashes():
    """Load existing hashes from the storage file."""
    hash_file_path = "hashes.json"
    if os.path.exists(hash_file_path):
        try:
            with open(hash_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading hashes file: File is empty or corrupted. Starting fresh.")
        except Exception as e:
            print(f"Unexpected error when reading hashes file: {e}")
    else:
        print("No existing hash file found. A new one will be created.")
    return {}

def update_hashes(file_path, checkpoint_name):
    """Update the hashes in the JSON file with the new checkpoint."""
    hash_value = hash_file(file_path)  # Recompute hash for current file state
    if hash_value:
        existing_hashes = load_existing_hashes()
        if file_path not in existing_hashes:
            existing_hashes[file_path] = {}
        existing_hashes[file_path][checkpoint_name] = hash_value

        try:
            with open("hashes.json", 'w') as file:
                json.dump(existing_hashes, file, indent=4)
            print(f"Hashes updated successfully under checkpoint: {checkpoint_name}")
        except Exception as e:
            print(f"Error updating hashes: {e}")
    else:
        print("Failed to hash file, cannot update checkpoint.")

def check_integrity(file_path, checkpoint_name):
    """Check the integrity of files against a specified checkpoint."""
    existing_hashes = load_existing_hashes()
    current_hash = hash_file(file_path)  # Recompute hash for current file state
    if current_hash and file_path in existing_hashes and checkpoint_name in existing_hashes[file_path]:
        stored_hash = existing_hashes[file_path][checkpoint_name]
        if current_hash == stored_hash:
            print(f"No changes detected for {file_path}")
        else:
            print(f"WARNING: File has been modified: {file_path}")
    else:
        print(f"WARNING: File not found in checkpoint or checkpoint missing.")

def monitor():
    file_path = input("Enter the file path to monitor: ").strip()
    print(f"Monitoring: '{file_path}'")

    while True:
        choice = input("Choose an option:\n1. Save checkpoint\n2. Check integrity\n3. Exit\n> ")
        if choice == "1":
            checkpoint_name = input("Enter checkpoint name: ")
            update_hashes(file_path, checkpoint_name)
        elif choice == "2":
            checkpoint_name = input("Enter the checkpoint name to check against: ")
            check_integrity(file_path, checkpoint_name)
        elif choice == "3":
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    monitor()
