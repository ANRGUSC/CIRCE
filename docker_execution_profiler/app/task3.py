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


    #output3 = filename.replace('.txt','')+"_3"
    output3 = 'output3.txt'
    
    input_path = os.path.join(pathin, 'output1.txt')
    output_path = os.path.join(pathout, output3)

    file_output = open(output_path, 'w')

    data = []
    with open(input_path,'r') as file_input:
        for line in file_input:
            data = line.strip().split(' ')
            data = sorted(data, reverse= True)
            for num in data:
                file_output.write(num+" ")
            file_output.write("\n")

    file_input.close()
    file_output.close()

    return output3
