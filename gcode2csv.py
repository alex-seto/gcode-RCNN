import os
import pandas as pd
import sys

def open_gcode_file(gcode_file):
    if gcode_file.endswith(".gcode"):
        try:
            with open(gcode_file, 'r') as r_f:
                raw_gcode = r_f.read()
            return raw_gcode
        except Exception as e:
            print(e)
            return None
    else:
        print("Not a gcode file, returning None")
        return None

def is_noncommand(line):
    return line == '' or line[0] == ';'

def get_unique_params(gcode_by_line):
    temp = {}
    for line in gcode_by_line:
        if is_noncommand(line):
            continue
        list_of_commands = line.split(';', 1)[0].split(' ')
        for elem in list_of_commands:
            if len(elem):
                if elem[0] not in temp:
                    temp[elem[0]] = 0
    return temp.keys()

def parse_command(line, UNIQUE_PARAMS):
    if is_noncommand(line):
        return 
    command = {param: None for param in UNIQUE_PARAMS}
    command_params = line.split(';', 1)[0].split(' ')
    for param in command_params:
        if len(param):
            command[param[0]] = param[1:]
    return pd.DataFrame(command, index = [0])

def parse_gcode(gcode_by_line, UNIQUE_PARAMS):
    gcode_df = pd.DataFrame(columns = UNIQUE_PARAMS)

    for line in gcode_by_line:
        command = parse_command(line, UNIQUE_PARAMS)
        if type(command) == pd.DataFrame:
            gcode_df = pd.concat([gcode_df, command],  axis = 0, ignore_index = 0)
    return gcode_df

def main(gcode_file, output_file):
    raw_gcode = open_gcode_file(gcode_file)
    if type(raw_gcode) != str:
        print("Error opening gcode")
    gcode_by_line = raw_gcode.split('\n')
    UNIQUE_PARAMS = get_unique_params(gcode_by_line)
    gcode_df = parse_gcode(gcode_by_line, UNIQUE_PARAMS)
    gcode_df.to_csv(output_file)
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide the correct amount of arguments")
    gcode_file = sys.argv[1]
    output_file = sys.argv[2]
    print("Parsing", gcode_file, "and saving output to", output_file)
    main(gcode_file, output_file)

