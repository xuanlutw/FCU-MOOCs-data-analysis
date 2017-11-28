import json
import time
import datetime

files = {'2014_all', '2015_all', '2016_all', '2017_all'}
i = 0
event = {'0'}
for f in files:
    current_file = open(f, 'r')
    for line in current_file:
        i += 1
        try:
            tmp_data = json.loads(line)
            event.add(tmp_data['event_type'])
        except:
            print('error')
        if (i % 10000) == 0:
            print(i)


j = 0
for k in event:
    j += 1
    print(k)
print('# of final event: ', j)
