# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .signals import check_good_worker
from crowd.turk.models import AmazonWorker
from crowd.utilities.models import TimeStampedModel


class Task(TimeStampedModel):
	title = models.CharField(_("Title"), max_length=255)
	question = models.CharField(_("Question"), max_length=1000)
	answers = models.ManyToManyField('AnswerOption')
	# gold = models.BooleanField(_("Gold task?"), default=False)


class TaskAssignment(TimeStampedModel):
	user = models.ForeignKey(AmazonWorker, related_name='task_assignments')
	task = models.ForeignKey(Task, related_name='assignments')
	user_answer = models.ForeignKey('AnswerOption', null=True)
	user_answer_time = models.DateTimeField(null=True)
	bias_at_answer = models.FloatField(_("bias"), default=0)
	gradient_at_answer = models.FloatField(_("Gradient"), default = 0)

	maximum = 10
	middle = 0
	minimum = -10
	unbiased_increment = 1
	stop_watermark_point_basis = 4
	behaviour_percent = 0.15
	anti_behaviour_percent = 0.2

	def __str__(self):
	    return self.id.__str__()

	def get_new_bias(self):
		if self.user_answer.correct:
			return self.new_bias_correct()
		else:
			return self.new_bias_incorrect()

	def new_bias_correct(self):
		print 'new_bias_correct'
		old_bias = self.user.bias
		if self.user.uncertain_count == 1:
			# 1st uncertain region
			return old_bias + self.unbiased_increment
		if old_bias < -self.stop_watermark_point_basis: 	# current negative bias
			d1 = abs(-self.maximum - old_bias)
			d2 = abs(self.middle - old_bias)
			d = d1 if d1>=d2 else d2
			return old_bias + self.anti_behaviour_percent*d
		else:												# current positive bias
			d = self.maximum - old_bias
			return old_bias + self.behaviour_percent*d

	def new_bias_incorrect(self):
		print 'new_bias_incorrect'
		old_bias = self.user.bias
		if self.user.uncertain_count == 1:
			return old_bias - self.unbiased_increment
		if old_bias >  self.stop_watermark_point_basis:		# current positive bias
			d1 = abs(self.maximum - old_bias)
			d2 = abs(self.middle - old_bias)
			d = d1 if d1>=d2 else d2
			return old_bias - self.anti_behaviour_percent*d
		else:												# current negative bias
			d = self.maximum + old_bias
			return old_bias - self.behaviour_percent*d

# post_save.connect(check_good_worker, sender=TaskAssignment)


class AnswerOption(TimeStampedModel):
	text = models.CharField(_("Answer option"), max_length=255)
	correct = models.BooleanField(default=False)

	def __str__(self):
	    return self.text
