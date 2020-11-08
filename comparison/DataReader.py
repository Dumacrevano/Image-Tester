
def datareader(filename):
    with open(filename) as inp:
        data = (inp.read().split('\n'))
    data_pool = []
    x = 0
    length = 0
    for i in data:
        if (x >= 1):
            arr_lines = i.split(',')
            entry = {'Name': arr_lines[0], 'RGB': "("  + arr_lines[1] + ", " + arr_lines[2] +  ", " + arr_lines[3] + ")",  'Type': arr_lines[4], 'Dimension': arr_lines[5],'BitDepth': arr_lines[6], 'Size':arr_lines[7], 'Signature':arr_lines[8]}
            data_pool.append(entry)
        else:
            length = int(i)
        x += 1
    inp.close()
    return data_pool, length

