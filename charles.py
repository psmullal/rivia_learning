"""List out files from directory."""
import sys
import os


def get_dir_listing(dirname: str) -> list:
    """
    Grab all the files in the provided directory name.

    Parameters: dirname (string).
    Returns: list of files.
    """

    for basename, dirs, files in (os.walk(dirname)):
        for fname in files:
            filenames.append(fname)
    return(filenames)


def main():
    """
    Main function.

    Parameters: None.
    Returns: None.
    """
    files_in_dir: list = []
    dirname: str = input("Please enter a DIRECTORY to process: ")
    if os.path.isdir(dirname):
        files_in_dir = get_dir_listing(dirname)
    else:
        print(f"The directory you entered ({dirname}) is not a directory.")
        sys.exit(1)
    for f in files_in_dir:
        print(f"{dirname} => {f}")
    sys.exit()


if __name__ == "__main__":
    main()