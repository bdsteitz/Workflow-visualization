import string
from django import forms
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from display.models import Task 

class SwitchGraphForm(forms.Form):
    switch_graph = forms.ChoiceField(label='View Day:', required=False)

    helper = FormHelper()
    helper.form_id = 'switch-graph-form'
    helper.form_class = 'form-inline'
    helper.form_method = 'GET'
    helper.help_text_inline = True
    helper.error_text_inline = True
    helper.form_show_labels = True
    helper.field_template = 'display.html'

    def __init__(self, *args, **kwargs):
        letters = list(string.ascii_uppercase)

        date = kwargs.pop('date')
        super(SwitchGraphForm, self).__init__(*args, **kwargs)

        self.dates = Task.objects.values_list('appt_date', flat=True).distinct().order_by('appt_date')
        choices = [(reverse('display_home'), '---')] + [(reverse('display_date', args=[str(d)]), str(d)) for d in self.dates] #+ [(reverse('display_date', args=['2014-07-27']), 'sadflj')]
        self.fields['switch_graph'].choices = choices
        if date:
            self.fields['switch_graph'].initial = reverse('display_date', args=[date])

class SwitchDeptForm(forms.Form):
    dept = forms.ChoiceField(label='Department:', required=False)

    helper = FormHelper()
    helper.form_id = 'switch-graph-form2'
    helper.form_class = 'form-inline'
    helper.form_method = 'GET'
    helper.help_text_inline = True
    helper.error_text_inline = True
    helper.form_show_labels = True
    helper.field_template = 'display.html'

    def __init__(self, *args, **kwargs):
        letters = list(string.ascii_uppercase)

        date = kwargs.pop('date')
        dept = kwargs.pop('dept')
        super(SwitchDeptForm, self).__init__(*args, **kwargs)

	self.depts = Task.objects.values_list('addl_text', flat=True).distinct().order_by('addl_text')
	print self.depts
        choices = [(None, '---')] + [(reverse('display_date_dept', args=[str(date), str(d)]), d) for d in self.depts if len(d) > 0] 
        self.fields['dept'].choices = choices
	if dept:
        	self.fields['dept'].initial = reverse('display_date_dept', args=[date, dept])
	

    def getPatients(self):
        return self.patients

