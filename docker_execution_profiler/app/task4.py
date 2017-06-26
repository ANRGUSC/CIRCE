import os
import re

def task():


    outputD = os.path.join(os.path.dirname(__file__), 'output_D.txt')


    file_output = open(outputD, 'w')

    with open(os.path.join(os.path.dirname(__file__), 'output_C.txt'), 'r') as file_input:
        for line in file_input:
            file_output.write(line)
            file_output.write("task D file")

    file_input.close()
    file_output.close()

    return outputD