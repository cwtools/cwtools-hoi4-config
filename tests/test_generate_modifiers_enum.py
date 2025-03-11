import re

path_to_modifiers = "Config\\modifiers.cwt"


def generate_variables_enums():
    '''
    Extract modifiers from modifiers.cwt file and add them to enums based on their categories\n
    Separate enums for unit_leader modifiers, unit modifiers and everything else\n
    These enums are needed to add their support to modifier@modifier, leader_modifier@modifier and unit_modifier@modifier syntax\n
    '''
    with open(path_to_modifiers, 'r') as text_file:
        config_file = text_file.read().lower()
        modifiers = re.findall(r'\t([^ #]+) = (\w.*)', config_file)

        general_modifiers = []
        leader_modifiers = []
        unit_modifiers = []

        for i in modifiers:
            mod = i[0]
            category = i[1]

            if category == 'unit_leader':
                leader_modifiers.append(mod)

            elif category == 'army':
                unit_modifiers.append(mod)

            else:
                general_modifiers.append(mod)

        general_modifiers_enum = re.findall(r'\tenum\[general_modifiers_enum\] = \{.*?\}', config_file, flags=re.DOTALL | re.MULTILINE)[0]
        new_general_modifiers_enum = '\tenum[general_modifiers_enum] = {\n\t\t' + "\n\t\t".join(general_modifiers) + '\n\t}'
        new_config_file = config_file.replace(general_modifiers_enum, new_general_modifiers_enum)

        leader_modifiers_enum = re.findall(r'\tenum\[leader_modifiers_enum\] = \{.*?\}', config_file, flags=re.DOTALL | re.MULTILINE)[0]
        new_leader_modifiers_enum = '\tenum[leader_modifiers_enum] = {\n\t\t' + "\n\t\t".join(leader_modifiers) + '\n\t}'
        new_config_file = new_config_file.replace(leader_modifiers_enum, new_leader_modifiers_enum)

        unit_modifiers_enum = re.findall(r'\tenum\[unit_modifiers_enum\] = \{.*?\}', config_file, flags=re.DOTALL | re.MULTILINE)[0]
        new_unit_modifiers_enum = '\tenum[unit_modifiers_enum] = {\n\t\t' + "\n\t\t".join(unit_modifiers) + '\n\t}'
        new_config_file = new_config_file.replace(unit_modifiers_enum, new_unit_modifiers_enum)

    with open(path_to_modifiers, 'w') as text_file_write:
        text_file_write.write(new_config_file)


if __name__ == '__main__':
    generate_variables_enums()
