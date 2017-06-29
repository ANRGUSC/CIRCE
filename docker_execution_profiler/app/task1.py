"""
 * Copyright (c) 2016, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import os
import re



def task(filename, pathin, pathout):


    #output1 = filename.replace('.txt','') +"_1"
    output1 = 'output1.txt'

    input_path = os.path.join(pathin, filename)
    output_path = os.path.join(pathout, output1)


    file_output = open(output_path, 'w')

    with open(input_path, 'r') as file_input:
        for line in file_input:
            for n in line.strip().split(" "):
                num=int(n) 
                if num%2==0:
                    line = re.sub(re.compile(n+" *"),"", line)
            file_output.write(line)

    file_input.close()
    file_output.close()

    return output1

					


		
