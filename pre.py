import json
import os

current_total = 0
current_valid = 0
overall_total = 0
overall_valid = 0
target_file = open('output.json', 'w')

files = [f for f in os.listdir('./raw_data')]
files.sort()
for f in files:
    #print(f)
    current_file = open('./raw_data/' +  f, 'r')
    for line in current_file:
        try:
            tmp_data = json.loads(line)
            current_total = current_total + 1
            if (tmp_data['event_type'] == 'load_video') or (tmp_data['event_type'] == 'play_video') or (tmp_data['event_type'] == 'pause_video'):
                tmp = {}
                tmp_data2 = tmp_data['context']
                tmp_data3 = json.loads(tmp_data['event'])
                tmp['event_type'] = tmp_data['event_type']
                tmp['session'] = tmp_data['session']
                tmp['course_id'] = tmp_data2['course_id']
                tmp['time'] = tmp_data['time']
                tmp['user_id'] = tmp_data2['user_id']
                tmp['id'] = tmp_data3['id']
                tmp['code'] = tmp_data['page']
                #print(tmp)
                json.dump(tmp, target_file)
                target_file.write('\n')
                current_valid = current_valid + 1
        except:
            print('error, file: ', f, 'line: ', line)
    current_file.close()
    print(f, current_valid, '/', current_total)
    overall_valid += current_valid
    overall_total += current_total
    current_valid = 0
    current_total = 0
    current_valid = 0
print('done', overall_valid, '/', overall_total)
