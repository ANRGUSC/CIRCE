import os

def task():



    outputB = os.path.join(os.path.dirname(__file__), 'output_B.txt')

    file_output = open(outputB, 'w')

    data = []
    with open(os.path.join(os.path.dirname(__file__), 'output_A.txt'),'r') as file_input:
        for line in file_input:
            data.extend(map(int, line.strip().split(' ')))
    data = sorted(data)
    file_output.writelines( "%s " % item for item in data )

    file_input.close()
    file_output.close()

    return outputB