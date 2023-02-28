import os
import hashlib

# Function to calculate the SHA-256 hash of a file
def hash_file(filename):
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to find duplicate files in a directory and all its subdirectories
def find_duplicate_files(root_folder):
    # Dictionary to store the hashes and file paths of all files
    file_hashes = {}
    # List to store the duplicate files
    duplicates = []
    # Walk through the directory and all its subdirectories
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            # Get the full path of the file
            filepath = os.path.join(foldername, filename)
            # Calculate the SHA-256 hash of the file
            file_hash = hash_file(filepath)
            # Check if the hash already exists in the dictionary
            if file_hash in file_hashes:
                # Add the current file to the list of duplicates
                duplicates.append(filepath)
            else:
                # Add the hash and file path to the dictionary
                file_hashes[file_hash] = filepath
    return duplicates

# Function to delete duplicate files
def delete_duplicate_files(duplicates):
    total_saved = 0
    for filepath in duplicates:
        # Get the size of the file
        file_size = os.path.getsize(filepath)
        # Delete the file
        os.remove(filepath)
        # Add the size of the file to the total saved
        total_saved += file_size
    return total_saved

# Main function
def main():
    # Get the directory to scan for duplicates
    root_folder = input("Enter the directory to scan for duplicates: ")
    # Find the duplicate files
    duplicates = find_duplicate_files(root_folder)
    if len(duplicates) == 0:
        print("No duplicate files found.")
    else:
        # Calculate the total size of the duplicate files
        total_size = sum(os.path.getsize(filepath) for filepath in duplicates)
        # Convert the size to a more readable format
        total_size_str = "{:.2f} MB".format(total_size / 1024 / 1024)
        print("Found {} duplicate files with a total size of {}.".format(len(duplicates), total_size_str))
        # Ask the user if they want to delete the duplicate files
        choice = input("Do you want to delete all duplicate files? (y/n): ")
        if choice.lower() == 'y':
            # Delete the duplicate files
            total_saved = delete_duplicate_files(duplicates)
            # Convert the saved size to a more readable format
            total_saved_str = "{:.2f} MB".format(total_saved / 1024 / 1024)
            print("Deleted all duplicate files. Saved {} of disk space.".format(total_saved_str))
        else:
            print("No files were deleted.")

if __name__ == "__main__":
    main()

