import re
import glob
import json

path_to_config = "Config\\"
path_to_documentation = "Config\\script_documentation.json"

FALSE_POSITIVES = [
    'career_profile',
    'building_count_trigger',
    'resource_count_trigger',
    'ideology_support_trigger',
]


def check_missing_triggers():
    '''
    Validate .cwt files with triggers against documentation file (script_documentation.json)\n
    Triggers are defined in .cwt files with 'alias[trigger:xxx]' syntax\n
    Script will print triggers that are defined in documentation but not in .cwt files\n
    Triggers can be added to ignore by including them into FALSE_POSITIVES list
    '''
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

    raise_error = False
    if len(results_missing_triggers) > 0:
        for i in results_missing_triggers:
            if [_ for _ in FALSE_POSITIVES if _ in i] == []:
                print(f'- [] - {i}')
                raise_error = True
        if raise_error:
            raise Exception("There are triggers in documentation file that are not present in .cwt files")

    print("No missing triggers found. Good job!")


if __name__ == '__main__':
    check_missing_triggers()
