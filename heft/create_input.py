import re


def init(filename):
    """
    This function read the tgff file and
    build computation matrix, communication matrix, rate matrix.
    TGFF is a useful tool to generate directed acyclic graph, tfgg file represent a task graph.
    """
    f = file(filename, 'r')
    f.readline()
    f.readline()
    f.readline()

    # Calculate the amount of tasks
    num_of_tasks = 0
    while f.readline().startswith('\tTASK'):
        num_of_tasks += 1
    #print 'Number of tasks = %d' % num_of_tasks

    # Build a communication matrix
    data = [[-1 for i in range(num_of_tasks)] for i in range(num_of_tasks)]
    line = f.readline()
    while line.startswith('\tARC'):
        line = re.sub(r'\bt\d_', '', line)
        A = [int(s) for s in line.split() if s.isdigit()]
        i, j, d = [int(s) for s in line.split() if s.isdigit()]
        data[i][j] = d
        line = f.readline()
    #for line in data:
    #    print line


    while not f.readline().startswith('@computation_cost'):
        pass

    # Calculate the amount of processors
    num_of_processors = len(f.readline().split()) - 3
    #print 'Number of processors = %d' % num_of_processors

    # Build a computation matrix
    comp_cost = []
    line = f.readline()
    while line.startswith('  '):
        comp_cost.append(map(int, line.split()[-num_of_processors:]))
        line = f.readline()
    #for line in comp_cost:
    #    print line

    # Build a rate matrix
    rate = [[1 for i in range(num_of_processors)] for i in range(num_of_processors)]
    for i in range(num_of_processors):
        rate[i][i] = 0

    # Build a network profile matrix
    quaratic_profile = [[(0,0,0) for i in range(num_of_processors)] for i in range(num_of_processors)]
    while not f.readline().startswith('@quadratic'):
        pass
    line = f.readline()
    line = f.readline()

    while line.startswith('  '):
        i,j = line.split()[0:2]
        a,b,c = [float(s) for s in line.split()[2:]]
        quaratic_profile[int(i[1])-1][int(j[1])-1] = tuple([a,b,c])
        line = f.readline()

    return [num_of_tasks, num_of_processors, comp_cost, rate, data, quaratic_profile]