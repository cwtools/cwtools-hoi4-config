import re
import glob
import json

path_to_config = "Config\\"
path_to_documentation = "Config\\script_documentation.json"


def check_missing_variables():
    '''
    Validate .cwt files with variables against documentation file (script_documentation.json)\n
    Variables are defined in .cwt files inside 'value[variable]' block\n
    Script will print variables that are defined in documentation but not in .cwt files\n
    '''
    # 1 Extract variables from documentation
    documentation_dict = json.load(open(path_to_documentation))
    variables_dict_doc = {i: documentation_dict['dynamic_variables'][i].keys() for i in documentation_dict['dynamic_variables']}
    variables_list_doc = []
    # Create a single list with all variables
    for value in variables_dict_doc.values():
        for i in value:
            variables_list_doc.append(i)

    # 2 Extract variables from config files
    variables_list_config = []
    variable_block_pattern = r'value\[variable\] = \{.*?\}'
    variable_pattern = r'\t\t([^#\n\t]+)'
    for filename in glob.iglob(path_to_config + "**/*.cwt", recursive=True):
        with open(filename, 'r') as text_file:
            config_file = text_file.read()

            if 'value[variable] = {' in config_file and 'values = {' in config_file:
                variable_block = re.findall(variable_block_pattern, config_file, flags=re.DOTALL | re.MULTILINE)[0]
                pattern_matches = re.findall(variable_pattern, variable_block)
                if len(variable_block) > 0:
                    for match in pattern_matches:
                        variables_list_config.append(match)

    # 3 Perform a comparison
    results_missing_variables = []
    for var in variables_list_doc:
        var_encountered = False
        # Check direct match
        if var in variables_list_config:
            var_encountered = True
            continue
        # Check if there is a variable with target
        else:
            for i in variables_list_config:
                if i.startswith(f'{var}@'):
                    var_encountered = True
                    break
        if var_encountered is False:
            results_missing_variables.append(var)

    if len(results_missing_variables) > 0:
        for i in results_missing_variables:
            print(f'- [] - {i}')
        raise Exception("There are variables in documentation file that are not present in .cwt files")


if __name__ == '__main__':
    check_missing_variables()
