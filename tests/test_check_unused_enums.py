import re
import glob
from collections import Counter

path_to_config = "Config\\"


def check_unused_enums():
    '''
    Find all enums that are not used
    '''
    counter = Counter()
    effect_pattern = r'enum\[(.*?)\]'
    for filename in glob.iglob(path_to_config + "**/*.cwt", recursive=True):
        with open(filename, 'r') as text_file:
            config_file = text_file.read()

            if 'enum[' in config_file:
                pattern_matches = re.findall(effect_pattern, config_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        counter[match] += 1

    raise_error = False
    for i in counter:
        value = counter[i]
        if value == 1:
            print(f'- [] - {i}')
            raise_error = True

    if raise_error:
        raise Exception("There are unused enums in config files")

    print("No unused enums found. Good job!")


if __name__ == '__main__':
    check_unused_enums()
