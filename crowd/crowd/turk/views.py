from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse

from .models import AmazonWorker, HIT
from .functions import process_request
from .forms import TaskForm, PayCodeForm, PayAmazonForm


@xframe_options_exempt
def index(request):
	# latest_AmazonWorker_list = AmazonWorker.objects.order_by('-pub_date')[:5]
	template = 'turk/index.html'   
	hit_id = request.GET.get('hitId', None)	# find HIT in our db
	assignment_id = request.GET.get('assignmentId', None)	# create assignment
	submission_url = request.GET.get('turkSubmitTo', None)
	worker_id = request.GET.get('workerId', None)
	print hit_id, assignment_id, submission_url, worker_id
	behavior = 'R'
	preview = True
	form = PayCodeForm(initial={'worker_id': worker_id})
	pay_amazon_form = PayAmazonForm(initial={'assignmentId': assignment_id})

	if assignment_id != 'ASSIGNMENT_ID_NOT_AVAILABLE':
		try:
			hit = HIT.objects.get(hit_id=hit_id)
			print 'hit found'
		except HIT.DoesNotExist:
			hit = HIT.objects.get(hit_id=1)
		process_request(hit, assignment_id, submission_url, worker_id)
		behavior = hit.expected_bias
		preview = False

	context = {
		'preview': preview,
		'behavior': behavior,
		'worker_id': worker_id,
		'form': form,
		'pay_amazon_form': pay_amazon_form
	}
	return render(request, template, context)


@xframe_options_exempt
def question(request):
	from crowd.tasks.models import TaskAssignment, Task
	
	if request.method == 'POST':
		print request.POST
		worker_id = request.POST.get('worker_id', None)
		answer = request.POST.get('answer', None)
		task_assignment_id = request.POST.get('task_assignment_id', None)
		ta = TaskAssignment.objects.get(id=task_assignment_id)
		task = ta.task
		ta.user_answer = task.answers.get(text=answer)
		ta.save()
		url = request.get_full_path()
		return redirect(url + '?worker_id={0}'.format(worker_id))
	
	worker_id = request.GET.get('worker_id', None)
	template = 'turk/question.html'
	print 'worker_id ' + worker_id.__str__()
	try:
		worker = AmazonWorker.objects.get(aws_worker_id=worker_id)
	except AmazonWorker.DoesNotExist as e:
		return JsonResponse({'error': e.message})
	task_assignments = worker.task_assignments.filter(user_answer=None)
	ta = task_assignments[0]
	task = ta.task
	form = TaskForm(initial={'worker_id': worker_id, 'task_assignment_id': ta.id})
	context = {
		'worker_id': worker_id,
		'task': task,
		'form': form
	}
	return render(request, template, context)

@xframe_options_exempt
def pay_code_accept(request):
	worker_id = request.POST.get('worker_id', None)
	code = request.POST.get('code', None)
	try:
		decode = AmazonWorker.hashid.decode(code)[0]
	except IndexError:
		return JsonResponse({'status': 'error'})
	try:
		worker = AmazonWorker.objects.get(aws_worker_id=worker_id)
	except AmazonWorker.DoesNotExist:
		return JsonResponse({'status': 'error'})
	if decode == worker.id:
		return JsonResponse({'status': 'success'})
	return JsonResponse({'status': 'error'})
