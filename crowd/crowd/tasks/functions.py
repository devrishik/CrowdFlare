import random
import numpy as np

from .models import Task, TaskAssignment, AnswerOption


def get_random_numbers_for_file(randlist, rand_limit, file_limit):
    if len(randlist) == rand_limit:
        return  
    z = random.randint(0, file_limit-1)
    if not z in randlist:
        randlist.append(z)
    get_random_numbers_for_file(randlist, rand_limit, file_limit)


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
		f.close()
	return i + 1


def create_worker_task_assignments(worker):
	# get 20 news tasks
	news = 20
	non_news = 40 - news
	news_fname = 'crowd/news_website_list.txt'
	non_news_fname = 'crowd/non_news_website_list.txt'

	line_numbers = []
	get_random_numbers_for_file(line_numbers, news, file_len(news_fname))
	with open(news_fname) as f:
		lines = f.readlines()
		for x in line_numbers:
			try:
				task = Task.objects.get(question=lines[x])
			except Task.DoesNotExist:
				task = Task.objects.create(question=lines[x], title='Is this news?')
				task.answers.add(
					AnswerOption.objects.create(text="Yes", correct=True),
					AnswerOption.objects.create(text="No"))
				task.save()
			try:
				TaskAssignment.objects.get(user=worker, task=task)
			except TaskAssignment.DoesNotExist:
				TaskAssignment.objects.create(user=worker, task=task)
		f.close()

	# create non news tasks
	line_numbers = []
	get_random_numbers_for_file(line_numbers, non_news, file_len(non_news_fname))
	with open(non_news_fname) as f:
		lines = f.readlines()
		for x in line_numbers:
			try:
				task = Task.objects.get(question=lines[x])
			except Task.DoesNotExist:
				task = Task.objects.create(question=lines[x], title='Is this news?')
				task.answers.add(
					AnswerOption.objects.create(text="No", correct=True),
					AnswerOption.objects.create(text="Yes"))
				task.save()
			try:
				TaskAssignment.objects.get(user=worker, task=task)
			except TaskAssignment.DoesNotExist:
				TaskAssignment.objects.create(user=worker, task=task)
		f.close()


def update_gradient(task_assignment):
	print '```````update_gradient`````'
	print 'task_assignment' + str(task_assignment.id)

	# get TAs before this one
	task_assignments = task_assignment.user.task_assignments.filter(
		user_answer_time__lte=task_assignment.user_answer_time
		).exclude(user_answer=None).order_by('user_answer_time')
	if len(task_assignments) < 3:
		return
	biases = []
	r_task_assignments = task_assignments.reverse()[:3]
	for ta in r_task_assignments:
		biases += [ta.bias_at_answer]
	recent_bias = np.array(biases, dtype=np.float)
	gradients = np.gradient(recent_bias)

	prev_ta = r_task_assignments[1]
	prev_ta.gradient_at_answer = gradients[1]
	prev_ta.save()

