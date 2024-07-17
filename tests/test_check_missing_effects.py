import re
import glob
import json

path_to_config = "Config\\"
path_to_documentation = "Config\\script_documentation.json"

FALSE_POSITIVES = [
    'career_profile_step_missiolini',
    'reseed_division_commander',
]

# 1 Extract effects from documentation
documentation_dict = json.load(open(path_to_documentation))
list_with_effects_documentation = [i for i in documentation_dict['effects'].keys()]

# 2 Extract effects from config files
list_with_effects_config = []
effect_pattern = r'alias\[effect:(.*?)\]'
for filename in glob.iglob(path_to_config + "**/*.cwt", recursive=True):
    with open(filename, 'r') as text_file:
        config_file = text_file.read()

        if 'alias[effect:' in config_file:
            pattern_matches = re.findall(effect_pattern, config_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    list_with_effects_config.append(match)

# 3 Perform a comparison
list_with_effects_config = set(list_with_effects_config)
results_missing_effects = [i for i in list_with_effects_documentation if i not in list_with_effects_config]

raise_error = False
if len(results_missing_effects) > 0:
    for i in results_missing_effects:
        if [_ for _ in FALSE_POSITIVES if _ in i] == []:
            print(f'- [] - {i}')
            raise_error = True
    if raise_error:
        raise Exception("There are effects in documentation file that are not present in .cwt files")

if not raise_error:
    print("No missing effects found. Good job!")
