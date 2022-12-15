import argparse
import os
import csv

## parse args -----------------------------------------------------------------------
parser = argparse.ArgumentParser(description='adduser Test')
parser.add_argument('--id', default='./sid.csv', help='Image Directory')
args = parser.parse_args()

with open(args.id, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        cmd = f'python3 manage.py adduser {row[0]} {row[0]}@mail.yzu.edu.tw {row[0]}'
        print(cmd)
        os.system(cmd)
