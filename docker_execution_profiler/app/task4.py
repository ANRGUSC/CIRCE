import os
import re

def task(filename, pathin, pathout):


    #output4 = filename.replace('.txt','')+"_4"
    output4 = 'output4.txt'

    path_input=os.path.join(pathin, 'output2.txt')
    path_output=os.path.join(pathout, output4)

    file_output = open(path_output, 'w')

    with open(path_input, 'r') as file_input:
        for line in file_input:
            file_output.write(line)
            file_output.write("Task 4 has processed the file\n")

    file_input.close()
    file_output.close()

    return output4