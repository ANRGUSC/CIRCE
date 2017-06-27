import os
import re

def task():

  
    outputA = os.path.join(os.path.dirname(__file__), 'output_A.txt')

    file_output = open(outputA, 'w')

    with open(os.path.join(os.path.dirname(__file__), 'input.txt'), 'r') as file_input:
        for line in file_input:
            for n in line.strip().split(" "):
                num=int(n) 
                if num%2==0:
                    line = re.sub(re.compile(n+" *"),"", line)
            file_output.write(line)

    file_input.close()
    file_output.close()

    return outputA
					
