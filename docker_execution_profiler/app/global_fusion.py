# -*- coding: utf-8 -*
"""

"""
import admd
import os

def task(filelist, pathin, pathout):


    num = filelist[0].partition('f')[0]

    with open(os.path.join(pathout, num+'global_anomalies.log'), 'w') as outfile:
        for fname in filelist:
            with open(os.path.join(pathin,fname), 'r') as infile:
                for line in infile:
                    ano = line.split(";")
                    flow = ano[0]
                    ts = ano[1]
                    te = ano[2]
                    srcDst = flow.split()
                    srcIP, srcPort = srcDst[0].split(":")
                    dstIP, dstPort = srcDst[1].split(":")
                    ts = ts.split(".")
                    tsSec = int(ts[0])
                    tsUsec = int(ts[1])
                    te = te.split(".")
                    teSec = int(te[0])
                    teUsec = int(te[1])
                    tsS = admd.timestamp_t(sec=tsSec, usec=tsUsec)
                    tsE = admd.timestamp_t(sec=teSec, usec=teUsec)
                    str1 = ('{0};{1};{2}'.format(flow, tsSec, teSec))
                    #print(str1)
                    outfile.write(str1 + '\n')

    return num+'global_anomalies.log'


def main():

    filelist = ['1fusion_center0.log', '1fusion_center1.log', '1fusion_center2.log']
    outfile = task(filelist, os.path.dirname(__file__), os.path.dirname(__file__))
    return outfile

if __name__ == '__main__':

    filelist = ['1fusion_center0.log', '1fusion_center1.log', '1fusion_center2.log']
    task(filelist, os.path.dirname(__file__), os.path.dirname(__file__))
