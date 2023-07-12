import os
import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

num_dirs_searched = 0
num_files_searched = 0

def search_item_recursive(item_name, directory):
    global num_dirs_searched, num_files_searched
    found = False  # Flag to track if the item has been found

    for entry in os.scandir(directory):
        if entry.name == item_name:
            path = os.path.join(directory, entry.name)
            print("Path:", path)
            found = True

        if entry.is_dir() and not entry.name.startswith(('.', '..')):
            num_dirs_searched += 1
            found |= search_item_recursive(item_name, entry.path)
        else:
            num_files_searched += 1

    return found

def find_item_recursive(item_name, starting_directory):
    if not os.path.isdir(starting_directory):
        print("Invalid starting directory.")
        return

    print(f"Searching in: {Fore.GREEN}{starting_directory}{Style.RESET_ALL}")

    start_time = time.time()
    found = search_item_recursive(item_name, starting_directory)
    end_time = time.time()

    elapsed_time = end_time - start_time

    if not found:
        print("Item not found")

    print(f"\nTotal directories searched: {num_dirs_searched}")
    print(f"Total files searched: {num_files_searched}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

def get_current_directory():
    return os.getcwd()

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Invalid number of arguments.")
        print("Usage: python finder.py -file filename.ext OR python finder.py -folder foldername [starting_directory]")
        sys.exit(1)

    option = sys.argv[1]
    item_name = sys.argv[2]
    starting_directory = sys.argv[3] if len(sys.argv) == 4 else get_current_directory()

    if option == "-file" or option == "-folder":
        find_item_recursive(item_name, starting_directory)
    else:
        print("Invalid option.")
        print("Usage: python finder.py -file filename.ext OR python finder.py -folder foldername [starting_directory]")
