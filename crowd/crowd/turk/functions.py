from .models import AmazonWorker, Assignment, HIT


def process_request(behavior, hit_id, assignment_id, submission_url, worker_id):
	if behavior == 'good':
		expected_bias = AmazonWorker.GOOD
	if behavior == 'random':
		expected_bias = AmazonWorker.RANDOM
	if behavior == 'malicious':
		expected_bias = AmazonWorker.MALICIOUS
	worker, created = AmazonWorker.objects.get_or_create(
		aws_worker_id=worker_id)
	print worker.id
	hit = HIT.objects.get(hit_id=hit_id)
	print hit.id
	assignment, created = Assignment.objects.get_or_create(
		assignment_id=assignment_id,
		url_turk_submission=submission_url,
		user=worker,
		hit=hit)
	print assignment.id
	return None
