import csv
import json

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

t_lc = []
t_vwc = []
t_vcr = []
t_vwt = []
f_lc = []
f_vwc = []
f_vcr = []
f_vwt = []
fin2 = open('com.csv', 'r')
Q1 = csv.reader(fin2)
for row in Q1:
    try:
        if row[2] == 'T':
            t_lc.append(int(row[3]))
            t_vwc.append(int(row[4]))
            t_vcr.append(float(row[5]))
            t_vwt.append(int(row[6]))
        if row[2] == 'F':
            f_lc.append(int(row[3]))
            f_vwc.append(int(row[4]))
            f_vcr.append(float(row[5]))
            f_vwt.append(int(row[6]))
    except:
        haha = 0
print(max(t_lc), min(t_lc), mean(t_lc))
print(max(t_vwc), min(t_vwc), mean(t_vwc))
print(max(t_vcr), min(t_vcr), mean(t_vcr))
print(max(t_vwt), min(t_vwt), mean(t_vwt))
print(max(f_lc), min(f_lc), mean(f_lc))
print(max(f_vwc), min(f_vwc), mean(f_vwc))
print(max(f_vcr), min(f_vcr), mean(f_vcr))
print(max(f_vwt), min(f_vwt), mean(f_vwt))
fin2.close()
