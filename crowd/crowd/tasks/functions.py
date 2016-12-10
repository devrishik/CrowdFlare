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
	total = 20
	news = 10
	non_news = 20 - news
	news_fname = 'crowd/news_website_list.txt'
	non_news_fname = 'crowd/non_news_website_list.txt'


	# # line_numbers = []
	# # get_random_numbers_for_file(line_numbers, news, file_len(news_fname))
	news_line_numbers = [2, 1, 0, 12, 11, 6, 7, 13, 10, 26]
	# # line_numbers = []
	# # get_random_numbers_for_file(line_numbers, non_news, file_len(non_news_fname))
	n_news_line_numbers = [122, 42, 0, 26, 120, 47, 5, 125, 61, 64]

	with open(news_fname) as f1, open(non_news_fname) as f2:
		l1 = f1.readlines()
		l2 = f2.readlines()
		for x in range(total/2):
			t = n_news_line_numbers[x]
			d = news_line_numbers[x]
			try:
				task1 = Task.objects.get(question=l1[d])
			except Task.DoesNotExist:
				task1 = Task.objects.create(question=l1[d], title='Is this news?')
				task1.answers.add(
					AnswerOption.objects.create(text="Yes", correct=True),
					AnswerOption.objects.create(text="No"))
				task1.save()
			try:
				task2 = Task.objects.get(question=l2[t])
			except Task.DoesNotExist:
				task2 = Task.objects.create(question=l2[t], title='Is this news?')
				task2.answers.add(
					AnswerOption.objects.create(text="Yes", correct=True),
					AnswerOption.objects.create(text="No"))
				task2.save()
			x = random.random()
			tasks = [task1] + [task2]
			if x > 0.5:
				tasks.reverse()
			for task in tasks:
				try:
					TaskAssignment.objects.get(user=worker, task=task)
				except TaskAssignment.DoesNotExist:
					TaskAssignment.objects.create(user=worker, task=task)
	f1.close()
	f2.close()


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

