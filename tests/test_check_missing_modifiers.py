import json

path_to_config = "Config\\modifiers.cwt"
path_to_documentation = "Config\\script_documentation.json"

# FALSE_POSITIVES = [
#     'career_profile_step_missiolini',
#     'reseed_division_commander',
# ]

# 1 Extract effects from documentation
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

# # 2 Extract effects from config files
with open(path_to_config, 'r') as text_file:
    config_file = text_file.read()

    for key, values in modifiers_dict.items():
        for value in values:
            if f'{key} = {value}\n' not in config_file:
                results.append(f'{key} = {value}')

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
        raise Exception("There are effects in documentation file that are not present in .cwt files")

if not raise_error:
    print("No missing effects found. Good job!")
