import os
import re

def task(filename, pathin, pathout):


    #output5 = filename.replace('.txt','')+"_5"
    output5 = 'output5.txt'

    path_input=os.path.join(pathin, 'output4.txt')
    path_output=os.path.join(pathout, output5)

    file_output = open(path_output, 'w')

    with open(path_input, 'r') as file_input:
        for line in file_input:
            file_output.write(line)
            file_output.write("Task 5 has processed the file\n")

    file_input.close()
    file_output.close()

    return output5