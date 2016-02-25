# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from crowd.turk.models import AmazonWorker
from crowd.utilities.models import TimeStampedModel


class Task(TimeStampedModel):
	title = models.CharField(_("Title"), max_length=255)
	question = models.CharField(_("Question"), max_length=1000)
	answers = models.ManyToManyField('AnswerOption')


class TaskAssignment(TimeStampedModel):
	user = models.ForeignKey(AmazonWorker, related_name='task_assignments')
	task = models.ForeignKey(Task, related_name='assignments')
	user_answer = models.ForeignKey('AnswerOption', null=True)

	def __str__(self):
	    return self.id.__str__()


class AnswerOption(TimeStampedModel):
	text = models.CharField(_("Answer option"), max_length=255)
	correct = models.BooleanField(default=False)

	def __str__(self):
	    return self.text
