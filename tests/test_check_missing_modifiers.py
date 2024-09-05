import json

path_to_config = "Config\\modifiers.cwt"
path_to_documentation = "Config\\script_documentation.json"


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
            modifiers_dict[modifier['name']] = modifier['categories']
        # Dynamic modifier
        elif "groupname" in modifier.keys():
            pass

    # 2 Extract modifiers from config files
    with open(path_to_config, 'r') as text_file:
        config_file = text_file.read()

        # 3 Compare documentation and config
        for key, values in modifiers_dict.items():
            for value in values:
                if f'{key} = {value}\n' not in config_file:
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
