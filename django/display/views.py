from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

import json
import time

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

@login_required
def home(request):
	q = '''SELECT a.action_dt AS enter_time, b.action_dt AS exit_time, a.mrn AS id, b.mrn, 
	a.action_code, b.action_code, SUBSTR(a.display_text, 9) AS rooms, 
	SUBSTR(b.display_text, 9), a.addl_text, a.appt_idno, b.appt_idno, a.appt_date
        FROM display_task AS a, display_task AS b
        WHERE a.action_code = "I"
        AND b.action_code = "O"
        AND a.mrn = b.mrn
        AND SUBSTR(a.display_text, 9) = SUBSTR(b.display_text, 9)
        AND datetime(a.action_dt) < datetime(b.action_dt)
        AND a.addl_text = "Williamson Walk-In"
        ORDER BY a.mrn, a.action_dt, a.display_text, a.action_code ASC
	'''

	cur = connection.cursor()
	cur.execute(q)
	data = cur.fetchall()

	tasks = []
	i = 0
	patients = []
	mrn_to_i = {}
	for line in data:
		# {"startDate":new Date("Thurs Jun 12 13:54:00 EST 2014"),"endDate":new Date("Thurs Jun 12 13:58:00 EST 2014"),"taskName":"Task 1","status":"Wait"},
		# print line

		mrn = line[2]
		if mrn not in mrn_to_i:
			mrn_to_i[mrn] = len(mrn_to_i.keys())
		i = mrn_to_i[mrn]
			
		t = {'startDate': int(time.mktime(line[0].timetuple())*1000), #line[0].strftime("%Y-%m-%d %H:%M:%S"), 
			'endDate': int(time.mktime(line[1].timetuple())*1000), #line[1].strftime("%Y-%m-%d %H:%M:%S"), 
			'taskName': 'Patient %d' % i, 
			'status': 'Inf' #status_dict[line[7]] if line[7] in status_dict else line[7] 
		}
		tasks.append(t)

	for i in sorted(mrn_to_i, key=lambda x: mrn_to_i[x]):
		patients.append('Patient %d' % mrn_to_i[i])

	c = {'tasks': json.dumps(tasks),
		'patients': json.dumps(patients)}

	return render(request, 'display.html', c)

def test(request):
	print 'hi'
	c = {}
	return render(request, 'blah.html', c)
