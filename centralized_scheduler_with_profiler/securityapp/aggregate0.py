"""
 * Copyright (c) 2017, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Pranak Sakulkar
 *      Jiatong Wang
 *      Aleksandra Knezevic
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

import os
import sys
import time

def task(onefile, pathin, pathout):

    time.sleep(20)

    filelist=[]
    filelist.append(onefile)

    num=filelist[0].partition('s')[0]

    with open(os.path.join(pathout, num+'merged_file0.ipsum'),'w') as outfile:
    	for filename in filelist:
            with open(os.path.join(pathin, filename), 'r') as infile:
                for line in infile:
                    outfile.write(line)


if __name__ == '__main__':

    filelist = ['1split_0']
    task(filelist, '/home/apac/security_app', '/home/apac/security_app')
