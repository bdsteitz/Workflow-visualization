from django.db import models

# Create your models here.


'''
appt date|column id|MRN|time stamp of action|action code|display text|addl text|appt idno|racfid|full name
2014-07-27| 68|004301230|2014-07-27 13:24:00|I|Put in: 6|Williamson Walk-In|76460152|chipbl1|ANTREASA CHIPA
'''
class Task(models.Model):
	appt_date = models.DateField()
	column_id = models.IntegerField()
	mrn = models.IntegerField()
	action_dt = models.DateTimeField()
	action_code = models.CharField(max_length=16)
	display_text = models.CharField(max_length=128)
	addl_text = models.CharField(max_length=128)
	appt_idno = models.IntegerField()
	racfid = models.CharField(max_length=32)
	full_name = models.CharField(max_length=128)
	

