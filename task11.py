def open_file(m: str) -> list:
    try:
        with open(m, 'r') as fh:
            return(fh.readlines())
    except FileNotFoundError:
        return("ERROR: file does not exist.")


def read_file():
    user_file = input("Please enter file to read: ")
    try:
        file_contents = open_file(user_file)
    except:
        print(f"There was an error trying to open {user_file}. Please re-run and try again.")
        sys.exit(1)
    all_vowel_count, uniq_vowels, vowels = count_vowels(file_contents)
    print_results(user_file, all_vowel_count, uniq_vowels, vowels)


def print_results(user_file: str, all_vowel_count: int, uniq_vowels: int, 
                  vowels: dict, output_file='vowel_search_results.txt'):
    title = f" Vowel Search Report - {user_file} "
    padding = '*' * 10
    with open(output_file, 'a+') as fh:
        full_title = f"{padding}{title}{padding}\n"
        fh.write(full_title)
        fh.write("-" * (len(full_title)-1))
        fh.write("\n")
        fh.write(f"Unique Vowels Found: {len(uniq_vowels)}\n")
        fh.write(f"Number of Times Vowels Appear in File: {all_vowel_count}\n")
        for vowel in vowels.keys():
            fh.write(f"{vowel.upper()}:\t{vowels[vowel]}\n")
        fh.write("\n")

    
def count_vowels(file_contents: list) -> tuple:
    all_vowel_count: int = 0
    uniq_vowels: set = set()
    vowels: dict = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u':0 }
    for line in file_contents:
        for letter in line:
            if letter in vowels.keys():
                all_vowel_count += 1
                vowels[letter] += 1
                uniq_vowels.add(letter)
    
    return all_vowel_count, uniq_vowels, vowels

if __name__ == "__main__":
    read_file()