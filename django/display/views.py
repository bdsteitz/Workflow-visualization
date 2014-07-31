from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from display.forms import SwitchGraphForm, SwitchDeptForm
from display.models import Task

import json
import time
import datetime

# Create your views here.
status_dict = {
	'BR-WR':'Wait', 
	'LabWR':'Wait', 
	'TVWR':'Wait', 
	'InfWR':'Wait', 
	'Lunch':'Wait', 
	'IR':'Intake', 
	'DR':'DR',
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

	if 'sorted' in request.GET:
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
		room = line[7]
		if len(room) == 0: continue
		rooms.add(room)

		if 'left_align' in request.GET:
			base_time = int(time.mktime(datetime.datetime.now().timetuple()))
			end_val = base_time + (end_val - start_val)
			start_val = base_time
			#print start_val, end_val

		t = None
		if 'by_room' in request.GET:
			t = {'startDate': start_val,
				'endDate': end_val,
				'taskName': room,
				'status': 'room'
			}
		else:
			t = {'startDate': start_val,
				'endDate': end_val,
				'taskName': 'Patient %d' % i, 
				'status': status_dict[line[7]] if line[7] in status_dict else line[7] 
			}
		tasks.append(t)

	for i in sorted(mrn_to_i, key=lambda x: mrn_to_i[x]):
		patients.append('Patient %d' % mrn_to_i[i])

	if 'by_room' in request.GET:
		task_names = sorted(list(rooms))
	else:	
		task_names = patients
	
	return (tasks, task_names)

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
	print task_names

	c = {'tasks': json.dumps(tasks),
		'task_names': json.dumps(task_names),
		'form': form,
		'form2': form2,
		'scale': (len(task_names) - 100) / 25 if len(task_names) > 100 else 0
	}
	return render(request, 'display.html', c)


'''SELECT a.appt_date, a.mrn, a.addl_text,  SUBSTR(a.display_text, 9), a.action_dt AS enter_time, b.action_dt - a.action_dt as timeDifference, b.action_dt AS exit_time, a.appt_idno
FROM display_task a, display_task b
WHERE a.appt_idno = b.appt_idno
AND a.mrn = b.mrn
AND a.action_dt < b.action_dt
AND a.addl_text = b.addl_text
AND SUBSTR(a.display_text, 9) = SUBSTR(b.display_text, 9)
AND a.appt_date = b.appt_date
AND a.appt_date = '2014-06-12'
AND a.addl_text = '100 Oaks Breast Center Infusion'
'''

def test(request):
	print 'hi'
	c = {}
	return render(request, 'blah.html', c)
