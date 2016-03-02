from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
    	from crowd.tasks.models import Task
        model = Task
        fields = ('title', 'question', 'answers')
