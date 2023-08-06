

import csv


def read_csv(file, mode='r'):
    """
    read from csv file
    :param file: csv file path
    :param mode: [select]   read format.  defalut:r
    :return: array []
    """
    data = []
    with open(file, mode, encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            data.extend(row)
    return data

def write_csv(file, data, mode='r'):
    """
    write data into csv file
    :param file: save file path
    :param data: data format: [[],[],[]]
    :param mode: [select]   save format.  defalut:r
    :return: None
    """

    with open(file, mode, encoding='utf-8') as f:
        csv_writer = csv.writer(f, lineterminator='\n')
        csv_writer.writerows(data)




def read_minibatch(file):
    data = read_csv(file)
    arr = []
    num = 1
    i = 1
    for line in data:
        num += 1
        i += 1
        arr.append(line)
        if num > 1000 or i > len(data):
            yield arr
            arr = []
            num = 1
