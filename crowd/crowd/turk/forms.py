from django import forms


class TaskForm(forms.Form):
	CHOICES = [
		('yes', 'Yes'),
		('no', 'No')]
	answer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	worker_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
	task_assignment_id = forms.CharField(max_length=255, widget=forms.HiddenInput())


class PayCodeForm(forms.Form):
	worker_id = forms.CharField(max_length=255, widget=forms.HiddenInput())
	code = forms.CharField(max_length=255, label='Code')	


class PayAmazonForm(forms.Form):
	assignmentId = forms.CharField(max_length=255, widget=forms.HiddenInput())	
