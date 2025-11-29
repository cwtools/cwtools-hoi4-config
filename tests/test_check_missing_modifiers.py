import json
import re

path_to_config = "Config\\modifiers.cwt"
path_to_documentation = "Config\\script_documentation.json"

FALSE_POSITIVES = [
    '<ModifierStatValue>_value_factor',
    'module_<EquipmentModule>_design_cost_factor',
]


def check_missing_modifiers():
    '''
    Validate .cwt files with modifiers against documentation file (script_documentation.json)\n
    Modifiers are defined in modifier.cwt files with 'xxx = category' syntax\n
    Script will print modifiers that are defined in documentation but not in .cwt files\n
    '''
    # 1 Extract static modifiers from documentation
    documentation_dict = json.load(open(path_to_documentation))
    documentation = [i for i in documentation_dict['modifiers']]
    modifiers_dict = {}
    results = []

    for modifier in documentation:
        # Static modifier
        if "name" in modifier.keys():
            if modifier['name'] in FALSE_POSITIVES:
                continue
            modifiers_dict[modifier['name']] = modifier['categories']
        # Dynamic modifier
        elif "groupname" in modifier.keys():
            if modifier['groupname'] in FALSE_POSITIVES:
                continue
            modifiers_dict[modifier['groupname']] = modifier['categories']

    # 2 Extract modifiers from config files
    with open(path_to_config, 'r') as text_file:
        config_file = text_file.read()

        # 3 Compare documentation and config
        for key, values in modifiers_dict.items():
            for value in values:
                # Dynamic modifier
                if "<" in key:
                    # Modifier starts with the token
                    if key[0] == '<':
                        stripped_key = key[key.index('>')+1:]
                        if f'{stripped_key} = {value}\n' not in config_file:
                            results.append(f'{key} = {value}')
                    # Modifier ends with the token
                    elif key[-1] == '>':
                        stripped_key = key[:key.index('<')]
                        pattern = stripped_key + r'.*? = ' + value
                        pattern_matches = re.findall(pattern, config_file)
                        if pattern_matches == []:
                            results.append(f'{key} = {value}')
                    # Token is somewhere in the middle of the modifier
                    else:
                        splitted_key = key.split('<')
                        key1 = splitted_key[0]
                        key2 = splitted_key[1][splitted_key[1].index('>')+1:]
                        pattern = key1 + r'.*?' + key2 + r' = ' + value
                        pattern_matches = re.findall(pattern, config_file)
                        if pattern_matches == []:
                            results.append(f'{key} = {value}')
                elif f'{key} = {value}\n' not in config_file:
                    results.append(f'{key} = {value}')

    # 4 Format the results
    raise_error = False
    if len(results) > 0:
        # Strip and split each line into (key, value) tuples
        key_value_pairs = [line.split(" = ") for line in results]
        # Sort first by value and then by key, both alphabetically
        sorted_pairs = sorted(key_value_pairs, key=lambda x: (x[1], x[0]))
        for i in sorted_pairs:
            print(f'- [] - {i[0]} = {i[1]}')
        raise_error = True
        if raise_error:
            raise Exception("There are modifiers in documentation file that are not present in .cwt files")

    print("No missing modifiers found. Good job!")


if __name__ == '__main__':
    check_missing_modifiers()
