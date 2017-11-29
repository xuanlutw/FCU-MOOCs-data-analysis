import csv
import json

fin1 = open('feature.json', 'r')
feature = {}
for line in fin1:
    tmp_data = json.loads(line)
    key = (tmp_data['Course_id'], tmp_data['User_id'])
    feature[key] = tmp_data
    feature[key].pop('Course_id')
    feature[key].pop('User_id')
fin1.close()
fin2 = open('hack_question02.csv', 'r')
fout = open('hack_question02_done.csv', 'w')
Q1 = csv.reader(fin2)
w = csv.writer(fout)
for row in Q1:
    try:
        if row[0] == 'course_id':
            continue
        row.append(feature[(row[0], int(row[1]))]['Login_count'])
        row.append(feature[(row[0], int(row[1]))]['Video_watch_count'])
        row.append(feature[(row[0], int(row[1]))]['Video_complete_rate'])
        row.append(feature[(row[0], int(row[1]))]['Video_watch_time'])
        #print(row)
        w.writerow(row)
    except:
        row.append('NULL')
        row.append('NULL')
        row.append('NULL')
        row.append('NULL')
        print(row[2])
        #print(row)
        w.writerow(row)
fin2.close()
fout.close()
