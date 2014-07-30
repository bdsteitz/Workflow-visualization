import os
import datetime
import string

from display.models import Task
from django.utils import timezone


# python manage.py runscript load --script-args=path to file
def usage():
	print 'python manage.py runscript load --script-args=path to file'
	exit()

def run(*script_args):
	if len(script_args) != 1:
		usage()

	path = script_args[0]
	if os.path.exists(path) == False:
		raise Exception('Given path does not exist: %s' % dir_path)

	Loader(path).load()

class Loader:
	def __init__(self, path):
		self.path = path

	def load(self):
		print 'Loading from %s ...' % self.path

		f = open(self.path, 'r')
		lines = f.readlines()
		f.close()
	
		to_insert = []	
		i = 0
		for line in lines:
			if i == 0:
				i += 1
				continue

			s = line.split('|')
			assert len(s) == 10

			t = Task()
			appt_date = datetime.datetime.strptime(s[0], "%Y-%m-%d")
			t.appt_date = timezone.make_aware(appt_date, timezone.get_default_timezone())
			t.column_id = int(s[1])
			t.mrn = int(s[2])
			action_dt = datetime.datetime.strptime(s[3], "%Y-%m-%d %H:%M:%S")
			t.action_dt = timezone.make_aware(action_dt, timezone.get_default_timezone())
			t.action_code = s[4]
			t.display_text = s[5]
			t.addl_text = string.strip(s[6])
			for c in string.punctuation:
				t.addl_text = t.addl_text.replace(c, '')

			t.appt_idno = int(s[7]) if len(s[7]) > 0 else -1
			t.racfidc = s[8]
			t.full_name = s[9]

			to_insert.append(t)
			i += 1
	
		Task.objects.bulk_create(to_insert)
		print 'Inserted %d tasks' % len(to_insert)

		


