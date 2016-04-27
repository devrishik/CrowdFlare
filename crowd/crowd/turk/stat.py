for a in AmazonWorker.objects.all():
	ass = a.assignment_set.all()[0]
	l = []
	l += ass.hit.expected_bias.__str__()
	l += [a.aws_worker_id.__str__()]
	l += [ass.created.__str__()]
	qs = list(TaskAssignment.objects.filter(user=a, created__range=["2016-04-22", "2016-04-28"]).exclude(user_answer=None))
	if len(qs) > 25:
		for ta in qs:
		    l += [ta.user_answer.correct, ta.bias_at_answer]
		    if qs.index(ta) == len(qs)-1:
		    	l += [ta.user_answer_time.__str__()]
	wr.writerow(l)


sum = 0
count = 0
for hit in HIT.objects.filter(expected_bias='R'):
	print 'hit', hit.id
    for ass in hit.assignment_set.all():
    	if ass.user.task_assignments.exclude(user_answer=None).filter(created__range=["2016-04-22", "2016-04-28"]).count() > 25:
    		sum += ass.user.bias
    		count += 1
    		print ass.user.bias

correct = 0
incorrect = 0
for hit in HIT.objects.filter(expected_bias='R'):
	print 'hit', hit.id
    for ass in hit.assignment_set.all():
    	qs = ass.user.task_assignments.exclude(user_answer=None).filter(created__range=["2016-04-22", "2016-04-28"])
    	print len(qs)
    	if len(qs) > 25:
    		for ta in qs:
    			if ta.user_answer.correct:
    				correct += 1
    			else:
    				incorrect += 1