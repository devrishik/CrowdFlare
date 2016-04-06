import random

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
	non_news = 50 - news
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

