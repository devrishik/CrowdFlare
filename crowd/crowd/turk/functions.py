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
