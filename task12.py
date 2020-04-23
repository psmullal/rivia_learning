import sys
import os


def check_file_readiness(filename: str, mode='r') -> bool:
    '''
    Summary: Check for the existence of a file.
    If the file doesn't exist, check the permissions of the parent directory
    Parameters: filename (string)
    Variables:
        filename What we are checking
        parent_dir In the case of the file missing check write capability
    Returns:
        bool
    '''

    if os.path.exists(filename):  # The _path_ exists
        if os.path.isfile(filename):  # is it a file or a dir
            if mode == 'r':
                return os.access(filename, os.R_OK)
            else:
                return os.access(filename, os.W_OK)
        else:
            return False  # path is a directory
    parent_dir: str = os.path.dirname(filename)
    if not parent_dir:
        parent_dir = '.'  # if parent is writable, we can write a file
    return os.access(parent_dir, os.W_OK)


def read_file(arguments: dict):
    '''
    Summary:
        Take in the sys.argv dictionary, process the input file, write output
    Parameters:
        arguments: passed from sys.argv
    Variables:
        user_file is the source (read) file
        output_file is the output (write) file
    Returns: None
    '''

    user_file: str = arguments[1]  # First parameter, should be read filename.
    output_file: str = arguments[2]  # Should be the write file name.
    print(f"Checking readability of {user_file}")

    if check_file_readiness(user_file, 'r'):
        try:
            with open(user_file, 'r') as fh:
                file_contents: str = fh.read()
        except IOError as ioe:
            print(ioe)
            sys.exit(1)

        vowel_count, uniq_vowels, vowels = count_vowels(file_contents)
        print_results(user_file, vowel_count, uniq_vowels,
                      vowels, output_file)
    else:
        print(f"We encountered a file issue trying to read {user_file}")


def print_results(user_file: str, vowel_count: int, uniq_vowels: int,
                  vowels: dict, output_file='vowel_search_results.txt'):
    title = f" Vowel Search Report - {user_file} "
    padding = '*' * 10
    if check_file_readiness(output_file, 'w'):
        with open(output_file, 'a+') as fh:
            full_title = f"{padding}{title}{padding}\n"
            fh.write(full_title)
            fh.write("-" * (len(full_title)-1))
            fh.write("\n")
            fh.write(f"Unique Vowels Found: {len(uniq_vowels)}\n")
            fh.write(f"Number of Times Vowels Appear in File: {vowel_count}\n")
            for vowel in vowels.keys():
                fh.write(f"{vowel.upper()}:\t{vowels[vowel]}\n")
            fh.write("\n")
    else:
        error_str = '''
        There was an error with writing your output file '{}',
        Please check your permissions and try again.'''
        print(error_str.format(output_file))
        sys.exit(3)


def count_vowels(file_contents: list) -> tuple:
    all_vowel_count: int = 0
    uniq_vowels: set = set()
    vowels: dict = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
    for line in file_contents:
        for letter in line:
            if letter in vowels.keys():
                all_vowel_count += 1
                vowels[letter] += 1
                uniq_vowels.add(letter)

    return all_vowel_count, uniq_vowels, vowels


if __name__ == "__main__":
    if len(sys.argv) < 3:
        error_str = '''
        USAGE: {} <source filename> <output file>
        <source filename>:  Name of the source File.
        <output file>:      Name of the output File.
        '''
        print(error_str.format(sys.argv[0]))
        sys.exit(2)
    else:
        read_file(sys.argv)
