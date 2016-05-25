from django.conf import settings

from .models import AmazonWorker, Assignment, HIT
from crowd.tasks.functions import create_worker_task_assignments


def process_request(hit, assignment_id, submission_url, worker_id):
	try:
		worker = AmazonWorker.objects.get(aws_worker_id=worker_id)
		print 'found worker'
	except AmazonWorker.DoesNotExist:
		print 'creating worker'
		worker = AmazonWorker.objects.create(
			aws_worker_id=worker_id)

	print 'worker.id' + worker.id.__str__()
	assignment, created = Assignment.objects.get_or_create(
		assignment_id=assignment_id,
		url_turk_submission=submission_url,
		user=worker,
		hit=hit)
	print assignment.id, created

	if created:
		print 'created assignment'
		create_worker_task_assignments(worker)

	return None

def check_worker_uncertain_task_limit(worker_instance):
	print '`````check_worker_uncertain_task_limit`````'
	print 'bias = ' + worker_instance.bias.__str__()
	
	task_assignments = worker_instance.task_assignments.exclude(user_answer=None).exclude(bias_at_answer=0)
	if len(task_assignments) < settings.LONG_UNCERTAIN_SPAN_LIMIT:
		return False

	count = 0
	highest = 0
	for assignment in task_assignments:
		if assignment.bias_at_answer <= assignment.stop_watermark_point_basis:
			count += 1
			if highest < count:
				highest = count
		else:
			count = 0
	
	print 'count = ' + count.__str__()
	print 'highest = ' + highest.__str__()
	
	if highest <= 10:
		return False
	return True
