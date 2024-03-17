import csv

def readcsv(csvfile):

    reader = csv.reader(csvfile)
    
    data = list(reader)
    # for lines in reader:
    #     time_list.append(lines)

    return data