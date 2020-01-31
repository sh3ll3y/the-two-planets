"The Two Planets command line app."

import input_analyzer

from army_config import army_data
from army import Army
import data_validation
from input_analyzer import InputAnalyzer
from war_result_outputter import WarResultOutputter



def main(input_str):
    input_data = InputAnalyzer(input_str)
    if input_data.validate_input_format():
        enemy_army_name, enemy_battalions = input_data.analyzer.get_attack_details()

    if data_validation.validate_attack_data(enemy_army_name, enemy_battalions):
        home_army_name = army_data['enemies'][enemy_army_name]
        home_army = Army(home_army_name)
        home_army.prepare_battalions(enemy_battalions)
        output = WarResultOutputter(home_army)
        output.print_standard_output()


if __name__ == '__main__':
    input_str = input()
    main(input_str)
