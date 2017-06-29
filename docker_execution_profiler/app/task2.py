"""
 * Copyright (c) 2016, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import os


def task(filename, pathin, pathout):




    #output2 = filename.replace('.txt','')+"_2"
    output2 = 'output2.txt'

    input_path = os.path.join(pathin, 'output1.txt')
    output_path = os.path.join(pathout, output2)

    file_output = open(output_path, 'w')

    data = []
    with open(input_path,'r') as file_input:
        for line in file_input:
            data = line.strip().split(' ')
            data = sorted(data)
            for num in data:
                file_output.write(num+" ")
            file_output.write("\n")

    file_input.close()
    file_output.close()

    return output2




