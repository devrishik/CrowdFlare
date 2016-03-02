from .models import AmazonWorker, Assignment, HIT


def process_request(behavior, hit_id, assignment_id, submission_url, worker_id):
	if behavior == 'good':
		expected_bias = AmazonWorker.GOOD
	if behavior == 'random':
		expected_bias = AmazonWorker.RANDOM
	if behavior == 'malicious':
		expected_bias = AmazonWorker.MALICIOUS
	try:
		worker = AmazonWorker.objects.get(aws_worker_id=worker_id)
		print 'found worker'
	except AmazonWorker.DoesNotExist:
		print 'creating worker'
		worker = AmazonWorker.objects.create(
			aws_worker_id=worker_id,
			expected_bias=expected_bias)

	print worker.id
	hit = HIT.objects.get(hit_id=1)
	print hit.id
	assignment, created = Assignment.objects.get_or_create(
		assignment_id=assignment_id,
		url_turk_submission=submission_url,
		user=worker,
		hit=hit)
	print assignment.id

	if created:
		print 'created assignment'
		from crowd.tasks.models import TaskAssignment, Task
		tasks = Task.objects.all()
		for task in tasks:
			ta = TaskAssignment.objects.create(
				user=worker,
				task=task)

	return None
