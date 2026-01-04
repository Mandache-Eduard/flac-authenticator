import os
import sys

from external_tools import spek_manual
from run_modes import run_single_file, run_folder_batch

def main():
    # 0. Set instructions and manuals
    if len(sys.argv) < 2:
        print("Wrong number of arguments - check usage using 'py main.py help'")
        return

    elif sys.argv[1] == "help":
        print("Usage: py main.py <path_to_flac_file> (including .flac extension)")
        print("For example: python main.py X:\\path\\to\\file.flac")
        print("For Spek shortcuts use: python main.py spek_man")
        return

    if sys.argv[1] == "spek_man":
        spek_manual()
        return

    # 1. Get file path from command-line argument and determine running mode
    path = sys.argv[1]

    if os.path.isfile(path) and path.lower().endswith(".flac"):
        run_single_file(path, verbose=True, open_spek=True)

    elif os.path.isdir(path):
        run_folder_batch(path)

    else:
        print("Invalid file path or not a FLAC file.")
        return

if __name__ == "__main__":
    main()