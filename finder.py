import os
import sys
import time
from tqdm import tqdm
from treelib import Tree
from colorama import Fore, Style, init

# Initialize colorama
init()

def search_item_recursive(item_name, directory, tree):
    count = 0  # Number of files/folders searched
    copies = 0  # Number of copies found
    locations = []  # Locations where the item is found

    for root, dirs, files in os.walk(directory):
        count += 1
        if item_name in files or item_name in dirs:
            location = os.path.join(root, item_name)
            locations.append(location)
            copies += 1

    return locations, copies, count

def find_item_recursive(item_name, starting_directory, option):
    if not os.path.isdir(starting_directory):
        print("Invalid starting directory.")
        return

    tree = Tree()
    tree.create_node("/", "/")  # Add root node

    print(f"Searching in: {Fore.GREEN}{starting_directory}{Style.RESET_ALL}")

    with tqdm(total=0, unit="directory", bar_format="{l_bar}{bar} [ {elapsed}<{remaining}, {rate_fmt}]") as pbar:
        for root, dirs, files in os.walk(starting_directory):
            parent_node = os.path.dirname(root)
            if parent_node == starting_directory:
                parent_node = "/"

            if not tree.contains(parent_node):
                add_missing_parents(tree, parent_node)

            tree.create_node(os.path.basename(root), root, parent=parent_node)

            if option == "-file":
                locations, copies, count = search_item_recursive(item_name, root, tree)
                if copies > 0:
                    print(f"\n{Fore.YELLOW}Found {copies} copy(s) of '{item_name}' at the following location(s):")
                    for location in locations:
                        print(location)
                    break
            elif option == "-folder":
                if item_name in dirs:
                    result = os.path.join(root, item_name)
                    print(f"\n{Fore.YELLOW}Found: {result}{Style.RESET_ALL}")
                    break

            pbar.total += len(dirs)
            pbar.update()

    print(tree.show(line_type="ascii-em"))

    if option == "-file" and copies == 0:
        print(f"{Fore.RED}No copies of '{item_name}' found.{Style.RESET_ALL}")

    print(f"\nSearch completed in {int(time.time() - pbar.start_t)} seconds")
    print(f"Total number of files and folders searched: {pbar.total + 1}")

def add_missing_parents(tree, directory):
    if directory == "/":
        return

    parent = os.path.dirname(directory)
    if not tree.contains(directory):
        add_missing_parents(tree, parent)
        tree.create_node(os.path.basename(directory), directory, parent=parent)

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Invalid number of arguments.")
        print("Usage: python finder.py [option] item_name [starting_directory]")
        sys.exit(1)

    option = sys.argv[1]
    item_name = sys.argv[2]
    starting_directory = sys.argv[3] if len(sys.argv) == 4 else os.getcwd()

    if option == "-file" or option == "-folder":
        find_item_recursive(item_name, starting_directory, option)
    else:
        print("Invalid option.")
        print("Usage: python finder.py [option] item_name [starting_directory]")
