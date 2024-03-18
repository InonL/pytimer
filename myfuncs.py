import csv

def readcsv(csvfile):
    reader = csv.reader(csvfile)
    data = list(reader)
    return data