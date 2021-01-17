# !/usr/bin/env python
# ource_file = input("Enter filename to process: ")
source_file = 'cooker.py'
content = ''
try:
    with open(source_file, 'r') as fh:
        content = fh.read().lower()
except FileNotFoundError as e:
    print(f"There was an error, File not found: {e}")
except PermissionError as p:
    print(f"There was an error, you do not have permission to the file: {p}")


def count_vowels(content: str) -> dict:
    vowels = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
    # vowels = ['a', 'e', 'i', 'o', 'u']
    for v in vowels.keys():
        vowels[v] = content.count(v)
    return vowels


def write_output(vowels: dict, output_file_name='vowel_search_results.txt'):
    output_fmt = '''
  Unique Vowels Found: {}
  Number of times Vowels appeared in the file: {}
  A Count: {}
  E Count: {}
  I Count: {}
  O Count: {}
  U Count: {}
  '''
    unique_vowels = sum([x > 0 for x in vowels.values()])
    ttl_count = sum([x for x in vowels.values()])
    output_str = output_fmt.format(
                unique_vowels, ttl_count,
                vowels['a'] if vowels['a'] else 0,
                vowels['e'] if vowels['e'] else 0,
                vowels['i'] if vowels['i'] else 0,
                vowels['o'] if vowels['o'] else 0,
                vowels['u'] if vowels['u'] else 0
                )
    try:
        with open(output_file_name, 'w') as ofh:
            ofh.write(output_str)
    except PermissionError as p:
        print(f"""Would not write out file: {output_file_name},
Permission denied!\n {p}""")


vowel_count = count_vowels(content)
write_output(vowel_count)
