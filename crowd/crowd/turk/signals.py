# from .models import AmazonWorker


def upate_uncertain_count(sender, instance, **kwargs):
	from crowd.tasks.models import TaskAssignment as ta
	print 'upate_uncertain_count ' + str(instance.uncertain_count)
	print 'bias ' + str(instance.bias)
	
	if instance.uncertain_count == 5:
		# catch malicious
		print 'catch malicious'
		instance.set_exit_classification_bias(instance.bias, instance.MALICIOUS)
		return
	
	if abs(instance.bias) < ta.stop_watermark_point_basis and instance.uncertain_count == 1:
		from .functions import check_worker_uncertain_task_limit
		if check_worker_uncertain_task_limit(instance):
			# catch random
			print 'catch random'
			instance.set_exit_classification_bias(instance.bias, instance.RANDOM)
		return
	
	if abs(instance.bias) > ta.stop_watermark_point_basis and instance.uncertain_count in [1, 3]:
		instance.uncertain_count += 1
		print 'uncertain count = ' + instance.uncertain_count.__str__()
	
	if abs(instance.bias) < ta.stop_watermark_point_basis and instance.uncertain_count in [2, 4]:
		instance.uncertain_count += 1
		print 'uncertain count = ' + instance.uncertain_count.__str__()
	return