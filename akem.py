def main():
    source_file: str = input("Enter a file to analyze: ")
    content: str = ""

    try:
        with open(source_file, 'r') as fh:
            content = fh.read().lower()
    except FileNotFoundError:
        print("File cannot be found")
    except PermissionError:
        print("You don't have permissions")

    results: dict = count_vowels(content)
    
    write_report(results, source_file)

def count_vowels(content: str) -> dict:
    vowels = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

    for v in vowels.keys():
        vowels[v] = content.count(v)

    return vowels

    
# must have file name and something to write 
def write_report(results: dict, source_file: str, report_file: str = 'vowel_search_results.txt'): 
    output_fmt = '''
  {}
  {}
  Unique Vowels Found: {} ({})
  Number of times Vowels appeared in the file: {}
  A Count: {}
  E Count: {}
  I Count: {}
  O Count: {}
  U Count: {}
  {}
 '''
    unique_vowels = set()
    vowel_count: int = 0
    header_top = f"{'*' * 10} Vowel Search Report - "
    header_top += f"{source_file} {'*' * 10}"
    header_bottom = "{}".format("-" * len(header_top))
    
    for k in results.keys():
        vowel_count += results[k]
        if results[k] > 0:
            unique_vowels.add(k)
    # print(f"The unique vowels found are: {unique_vowels}")
    
    output_str: str = output_fmt.format(header_top,header_bottom, unique_vowels, len(unique_vowels), vowel_count,
        results['a'] if results['a'] else 0, 
        results['e'] if results['e'] else 0,
        results['i'] if results['i'] else 0,
        results['o'] if results['o'] else 0, 
        results['u'] if results['u'] else 0,
        header_bottom
        ) 
    
    # Build Text for output here
    # use a long string (like Aleks McKinney)
    # use the += modifiers (like Charles)
    # write one line at a time to the file as you build it. (bad choice, but still viable)
        # example: 
        #    total_vowels = sum(results.values())
        #    fh.write(f"Total Number of vowels: {total_vowels}\n")
    try:
        with open(report_file, 'a+') as fh:
            fh.write(output_str)
    except FileNotFoundError:
        print("File cannot be found")
    except PermissionError:
        print("You don't have permissions")


if __name__ == '__main__':
    main()