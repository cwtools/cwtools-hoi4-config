import re
import glob
import json

path_to_config = "Config\\"
path_to_documentation = "Config\\script_documentation.json"

# 1 Extract triggers from documentation
documentation_dict = json.load(open(path_to_documentation))
list_with_triggers_documentation = [i for i in documentation_dict['triggers'].keys()]


# 2 Extract triggers from config files
list_with_triggers_config = []
effect_pattern = r'alias\[trigger:(.*?)\]'
for filename in glob.iglob(path_to_config + "**/*.cwt", recursive=True):
    with open(filename, 'r') as text_file:
        config_file = text_file.read()

        if 'alias[trigger:' in config_file:
            pattern_matches = re.findall(effect_pattern, config_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    list_with_triggers_config.append(match)

# 3 Perform a comparison
list_with_triggers_config = set(list_with_triggers_config)
results_missing_triggers = [i for i in list_with_triggers_documentation if i not in list_with_triggers_config]

if len(results_missing_triggers) > 0:
    for i in results_missing_triggers:
        print(f'- [] - {i}')
    raise Exception("There are triggers in documentation file that are not present in .cwt files")
