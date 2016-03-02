from django.shortcuts import render

from .models import AmazonWorker
from .functions import process_request
from .forms import TaskForm


def index(request):
	# latest_AmazonWorker_list = AmazonWorker.objects.order_by('-pub_date')[:5]
	template = 'turk/index.html'
	behavior = request.GET.get('behavior', None)    
	hit_id = request.GET.get('hitId', None)	# find HIT in our db
	assignment_id = request.GET.get('assignmentId', None)	# create assignment
	submission_url = request.GET.get('turkSubmitTo', None)
	worker_id = request.GET.get('workerId', None)
	print hit_id, assignment_id, submission_url, worker_id
	context = {
		'behavior': request.GET.get('behavior', None),
		'aws_key': request.GET.get('aws_key', None),
		'error': process_request(behavior, hit_id, assignment_id, submission_url, worker_id),
		'question_url': "http://localhost:8000/turk/question/?workerId={0}&behavior={1}".format(worker_id, behavior)
	}
	return render(request, template, context)


def question(request):
	from crowd.tasks.models import TaskAssignment
	template = 'turk/question.html'
	worker_id = request.GET.get('workerId', None)
	worker = AmazonWorker.objects.get(aws_worker_id=worker_id)
	task_assignments = worker.task_assignments.filter(user_answer=None)
	ta = task_assignments[0]
	ques = ta.task
	context = {
		'ques': ques
	}
	return render(request, template, context)

