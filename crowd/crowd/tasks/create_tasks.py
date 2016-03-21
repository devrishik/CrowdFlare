from .models import Task, AnswerOption


i = 0
f = open('../website_list.txt')
for line in f.readlines():
	i++
	a1 = AnswerOption.objects.create(text='yes', correct=True)
	a2 = AnswerOption.objects.create(text='yes')
	t = Task.objects.create(title='Question '+i, question=line)
	t.answers.add(a1, a2)
