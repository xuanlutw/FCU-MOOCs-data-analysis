import json
import time
import datetime

student = {}
course = {}
files = {'2014.json', '2015.json', '2016.json', '2017.json'}
i = 0

for f in files:
    current_file = open(f, 'r')
    for line in current_file:
        i += 1
        tmp_data = json.loads(line)

    #do course
        if tmp_data['course_id'] in course:
            course[tmp_data['course_id']].add(tmp_data['id'])
        else:
            course[tmp_data['course_id']] = {tmp_data['id']}

    #do student
        t_now = datetime.datetime(*(time.strptime(tmp_data['time'][: 19], "%Y-%m-%dT%H:%M:%S"))[: 6])
        #print(t_now)
        if (tmp_data['course_id'], tmp_data['user_id']) in student:
            student[(tmp_data['course_id'], tmp_data['user_id'])]['Login_days'].add(tmp_data['time'][: 10])
            student[(tmp_data['course_id'], tmp_data['user_id'])]['Watched_video'].add(tmp_data['id'])
            if tmp_data['event_type'] == 'play_video':
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_session'] = tmp_data['session']
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_id'] = tmp_data['id']
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_time'] = t_now
            elif (tmp_data['event_type'] == 'pause_video' and
                    student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_session'] == tmp_data['session'] and
                    student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_id'] == tmp_data['id']):
                student[(tmp_data['course_id'], tmp_data['user_id'])]['Video_watch_time'] += (t_now - student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_time']).total_seconds()
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_session'] = ""
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_id'] = ""            
        else:
            student[(tmp_data['course_id'], tmp_data['user_id'])] = {'Login_days': {tmp_data['time'][: 10]}, 'Watched_video': {tmp_data['id']}, 'Video_watch_time': 0}
            if tmp_data['event_type'] == 'play_video':
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_session'] = tmp_data['session']
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_id'] = tmp_data['id']
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_time'] = t_now
            else:
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_session'] = ""
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_id'] = ""
                student[(tmp_data['course_id'], tmp_data['user_id'])]['pre_time'] = t_now
        if (i % 10000) == 0:
            print(i, '...done')
    current_file.close()

"""
key = course.keys()
for k in key:
    print(k, course[k])
"""

result = open('feature.json', 'w')
student_key = student.keys()
j = 0
for k in student_key:
    j += 1
    student[k]['Login_count'] = len(student[k]['Login_days'])
    student[k]['Video_watch_count'] = len(student[k]['Watched_video'])
    student[k]['Video_complete_rate'] = student[k]['Video_watch_count'] / len(course[k[0]])
    student[k].pop('pre_session')
    student[k].pop('pre_id')
    student[k].pop('pre_time')
    student[k].pop('Watched_video')
    student[k].pop('Login_days')
    student[k]['Course_id'] = k[0]
    student[k]['User_id'] = k[1]
    json.dump(student[k], result)
    result.write('\n')
    #print(k, student[k])
print('# of final data: ', j)
