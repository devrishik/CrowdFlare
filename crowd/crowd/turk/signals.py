# from .models import AmazonWorker


def upate_uncertain_count(sender, instance, **kwargs):
	from crowd.tasks.models import TaskAssignment as ta
	print 'upate_uncertain_count'
	if abs(instance.bias) > ta.stop_watermark_point_basis and instance.uncertain_count == 1:
		instance.uncertain_count += 1
		print 'uncertain count = 2'

