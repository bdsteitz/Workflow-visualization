from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from display.forms import SwitchGraphForm, SwitchDeptForm
from display.models import Task
from django.template.defaultfilters import register


import json
import time
import datetime
from collections import defaultdict

# Create your views here.
colors = ['#921600',
	'#CD820D',
	'#3A8408',
	'#000000',
	'#3E046F',
	'#666231',
	'#550000',
	'#003D00',
	'#04376F',
	'#008B8B',
	'#3D4557',
	'#63FA20',
	'#E820FA',
	'#0000FF',
	'#FAF720',
	'#FF3333',
	'#20FAD4',
	'#9932CC',
	'#FFFFFF',
	'#1E90FF']

abbr = {
        "O1" : "O-Flag",
	"A1" : "A-Flag",
	"P1" : "P-Flag",
	"D1" : "D-Flag",
	"R1" : "R-Flag",
	"C1" : "C-Flag",
	"S1" : "S-Flag",
	"X1" : "X-Flag",
	    "Exam" : "exam",
	    "Con" : "Consult",
	    "MM" : "Mammography",
	    "Wait" : "Waiting",
	    "Inf" : "Infusion",
	    "DR" : "DR",
	    "US" : "US",
	    "UBX" : "UBX",
	    "Stereo" : "Stereo",
	    "Intake" : "Intake",
	    "I1" : "I-Extra"
	}	

status_dict = {
        "O1" : "O-Flag",
	"A1" : "A-Flag",
	"E1" : "E-Flag",
	"P1" : "P-Flag",
	"D1" : "D-Flag",
	"R1" : "R-Flag",
	"C1" : "C-Flag",
	"S1" : "S-Flag",
	"X1" : "X-Flag",
	    "I1" : "I-Extra",
	    "MM" : "Mammography",
	    "Inf" : "Infusion",
	    "DR" : "DR",
	    "US" : "US",
	    "UBX" : "UBX",
	    "Stereo" : "Stereo",
	    "Intake" : "Intake",
	'BR-WR':'Wait', 
	'LabWR':'Wait', 
	'TVWR':'Wait', 
	'InfWR':'Wait', 
	'Lunch':'Wait', 
	'IR':'Intake', 
	'DR':'DR',
	'A': 'Exam',
	'B': 'Exam',
	'C': 'Exam',
	'A515':'Exam',
	'A516':'Exam',
	'A517':'Exam',
	'B518':'Exam',
	'B519':'Exam',
	'B520':'Exam',
	'B521':'Exam',
	'B522':'Exam',
	'B523':'Exam',
	'BD09':'Exam',
	'BXDR':'Exam',
	'C524':'Exam',
	'C525':'Exam',
	'C526':'Exam',
	'C527':'Exam',
	'C528':'Exam',
	'C529':'Exam',
	'C530':'Exam',
	'Con': 'Consult',
	'Con1':'Con',
	'Con2':'Con',
	'Con3':'Con',
	'Con4':'Con',
	'MM05':'MM',
	'MM42':'MM',
	'MM44':'MM',
	'MM46':'MM',
	'MM07':'MM',
	'MM43':'MM',
	'I-1':'Inf',
	'I-2':'Inf',
	'I-3':'Inf',
	'I-4':'Inf',
	'I-5':'Inf',
	'I-6':'Inf',
	'I-7':'Inf',
	'I-8':'Inf',
	'I-9':'Inf',
	'I-10':'Inf',
	'I-11':'Inf',
	'I-12':'Inf',
	'I-13':'Inf',
	'I-14':'Inf',
	'I-15':'Inf',
	'I-16':'Inf',
	'I': 'Infusion',
	'US-45':'US',
	'US45':'US',
	'US43':'US',
	'UBX-2':'UBX',
	'USBX':'UBX',
	'Stereo':'Stereo',
	'IR':'Intake',
	'IR47':'Intake',
	'I-Lab':'I',
	'RadCon':'Other',
	'MRI':'Other'
	}

def getData(request, dept, date):
	q = '''SELECT a.action_dt AS enter_time, b.action_dt AS exit_time, a.mrn AS id, b.mrn, 
	a.action_code, b.action_code, SUBSTR(a.display_text, 9) AS rooms, 
	SUBSTR(b.display_text, 9), a.addl_text, a.appt_idno, b.appt_idno, a.appt_date
        FROM display_task AS a, display_task AS b
        WHERE a.action_code = 'I'
        AND b.action_code = 'O'
        AND a.mrn = b.mrn
        AND SUBSTR(a.display_text, 9) = SUBSTR(b.display_text, 9)
        AND a.action_dt < b.action_dt
        AND a.addl_text = '%s'
	AND a.appt_date = '%s'
	AND b.appt_date = '%s'
	''' % (dept, date, date)
        #AND a.addl_text = "Williamson Walk-In"

	if 'sorted' in request.GET or 'left_align' in request.GET:
        	q += 'ORDER BY enter_time, a.mrn, a.action_dt, a.display_text, a.action_code ASC'
	else:
        	q += 'ORDER BY a.mrn, a.action_dt, a.display_text, a.action_code ASC'
	

	cur = connection.cursor()
	cur.execute(q)
	data = cur.fetchall()
	return data


def createTasks(request, data):
	tasks = []
	i = 0
	patients = []
	mrn_to_i = {}
	rooms = set()
	base_time = int(time.mktime(datetime.datetime.now().timetuple()))
	patient_base = {}
	for line in data:
		# {"startDate":new Date("Thurs Jun 12 13:54:00 EST 2014"),"endDate":new Date("Thurs Jun 12 13:58:00 EST 2014"),"taskName":"Patient 0","status":"Inf"}
		# print line

		mrn = line[2]
		if mrn not in mrn_to_i:
			mrn_to_i[mrn] = len(mrn_to_i.keys())
		i = mrn_to_i[mrn]
		
		delta = datetime.timedelta(hours=5)	
		start = line[0] + delta
		end = line[1] + delta
		start_val = int(time.mktime(start.timetuple()) * 1000)
		end_val = int(time.mktime(end.timetuple()) * 1000)
		room = parseRoom(line[7])
		if len(room) == 0: continue
		rooms.add(status_dict[room] if room in status_dict else room)

		if 'left_align' in request.GET:
			if mrn not in patient_base:
				patient_base[mrn] = start_val
			bt = patient_base[mrn]

			end_val = end_val - bt + base_time
			start_val = start_val - bt + base_time
			#print start_val, end_val

		t = None
		if 'by_room' in request.GET:
			t = {'startDate': start_val,
				'endDate': end_val,
				'taskName': status_dict[room] if room in status_dict else room,
				'status': 'room',
				'room': status_dict[room] if room in status_dict else room 
			}
		else:
			t = {'startDate': start_val,
				'endDate': end_val,
				'taskName': 'Patient %d' % i, 
				'status': status_dict[room] if room in status_dict else room 
			}
		tasks.append(t)

	for i in sorted(mrn_to_i, key=lambda x: mrn_to_i[x]):
		patients.append('Patient %d' % mrn_to_i[i])

	if 'by_room' in request.GET:
		task_names = sorted(list(rooms))
	else:	
		task_names = patients
	
	return (tasks, task_names)

def getStats(request, tasks):
	room_count = {}
	for t in tasks:
		start = t['startDate']
		end = t['endDate']
		if 'by_room' in request.GET:
			room = t['room']
		else:
			room = t['status']
		room = parseRoom(room)

		if room not in room_count:
			room_count[room] = 0
		room_count[room] += (end - start) / 1000

	for room in room_count:
		room_count[room] = float(room_count[room]) / 60
	return room_count

def getPie(stats, color_map):
	l = []
	for s in stats:
		l.append({'name': s, 'count': stats[s], 'color': color_map[s] if s in color_map else 'black'})
	return l

def parseRoom(room):
	init_room = room
	room = room.split('-')[0]
	room = room.split(' ')[0]
	for i in range(0, len(room)):
		if room[i].isdigit():
			return room[:i]
	if len(init_room) == 1:
		room += '1'

	if room in status_dict:
		return status_dict[room]

	return room

def getTaskToColor(stats):
	c = {}
	keys = stats.keys()
	for i in range(0, len(stats)):
		room = keys[i]
		if room in status_dict:
			c[status_dict[room]] = colors[i % len(colors)]
		else:
			c[room] = colors[i % len(colors)]
		
	return c	

@login_required
def home(request, date=None, dept=None):
	form2 = None
	if not date:
		task = Task.objects.values('appt_date', 'addl_text').order_by('-appt_date')[0]
		date = task['appt_date']
		dept = task['addl_text']	
		form2 = SwitchDeptForm(date=date, dept=dept)
		#print date, dept

	if not dept:
		task = Task.objects.values('addl_text').order_by('-appt_date')[0]
		dept = task['addl_text']	

	if date and dept:
		form2 = SwitchDeptForm(date=date, dept=dept)
		
	form = SwitchGraphForm(date=date)
	data = getData(request, dept, date)
	tasks, task_names = createTasks(request, data)
	stats = getStats(request, tasks)
	color_map = getTaskToColor(stats)

	c = {'tasks': json.dumps(tasks),
		'task_names': json.dumps(task_names),
		'form': form,
		'form2': form2,
		'scale': (len(task_names) - 100) / 25 if len(task_names) > 100 else 0,
		'stats': stats,
		'pie_data': json.dumps(getPie(stats, color_map)),
		'color_map': color_map,
		'colors': json.dumps(colors),
	}
	return render(request, 'display.html', c)

def test(request):
	print 'hi'
	c = {}
	return render(request, 'blah.html', c)

@register.filter(name='lookup')
def lookup(dict, index):
        if index in dict:
                return dict[index]
        return ''
