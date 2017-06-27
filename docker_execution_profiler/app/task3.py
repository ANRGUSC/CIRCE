import os
import re

def task():


    outputC = os.path.join(os.path.dirname(__file__), 'output_C.txt')


    file_output = open(outputC, 'w')

    with open(os.path.join(os.path.dirname(__file__), 'output_B.txt'), 'r') as file_input:
        for line in file_input:
            file_output.write(line)
            file_output.write("task C file")

    file_input.close()
    file_output.close()

    return outputC