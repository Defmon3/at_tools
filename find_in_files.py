#!/usr/bin/env python3
import sys
from collections import defaultdict


def main():
    # Check if file names are provided
    if len(sys.argv) < 2:
        print("Usage: python script.py file1.txt file2.txt ...")
        sys.exit(1)

    filenames = sys.argv[1:]  # Get the file names from command-line arguments
    item_files = defaultdict(set)  # Dictionary to store item and the files it appears in

    # Read each file and update item_files
    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                for line in file:
                    item = line.strip()
                    item_files[item].add(filename)
        except FileNotFoundError:
            print(f"File not found: {filename}")
            continue

    # Filter items that appear in more than one file and sort them
    items_multiple_files = {item: files for item, files in item_files.items() if len(files) > 1}
    sorted_items = sorted(items_multiple_files.items(), key=lambda x: len(x[1]), reverse=True)

    # Generate and print the report
    for item, files in sorted_items:
        print(f"'{item}' appears in {len(files)} files: {', '.join(files)}")


if __name__ == "__main__":
    main()
