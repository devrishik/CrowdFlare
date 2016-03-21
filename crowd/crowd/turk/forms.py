from django import forms


class TaskForm(forms.Form):
	CHOICES = [
		('yes', 'Yes'),
		('no', 'No')]
	answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	worker_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
	task_assignment_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
