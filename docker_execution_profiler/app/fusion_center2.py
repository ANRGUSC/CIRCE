# -*- coding: utf-8 -*
"""

"""
import admd
import os

def write_files(filename, fusion_center, pathout):
    with open(os.path.join(pathout, fusion_center), 'w') as f:
        for item in filename:
            f.write(item + '\n')

def task(filelist, pathin, pathout):

    num = filelist[0].partition('a')[0]

    simple_set = set()
    file1 = open(os.path.join(pathin,filelist[0]), 'r')
    for line in file1.readlines():
        str1 = line.strip()
        simple_set.add(str1)

    file1.close()

    astute_set = set()
    file2 = open(os.path.join(pathin,filelist[1]), 'r')
    for line in file2.readlines():
        str1 = line.strip()
        astute_set.add(str1)

    file2.close()

    print('len simple_set ', len(simple_set))
    print('len astute_set ', len(astute_set))

    set3 = simple_set & astute_set
    write_files(set3, num+'fusion_center2.log', pathout)
    return num+'fusion_center2.log'

def main():

    filelist = ['1anomalies_simple2.log', '1anomalies_astute2.log']
    outfile = task(filelist, os.path.dirname(__file__), os.path.dirname(__file__))
    return outfile


if __name__ == '__main__':

    filelist = ['1anomalies_simple2.log', '1anomalies_astute2.log']
    task(filelist, os.path.dirname(__file__), os.path.dirname(__file__))
