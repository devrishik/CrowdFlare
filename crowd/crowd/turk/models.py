# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from crowd.users.models import User
from crowd.utilities.models import TimeStampedModel
from .signals import upate_uncertain_count

from hashids import Hashids


class AmazonWorker(TimeStampedModel):
	"""Worker from Amazon"""
	hashid = Hashids(salt=settings.SECRET_KEY, min_length=16)
	GOOD = 'G'
	RANDOM = 'R'
	MALICIOUS = 'M'
	CLASSIFICATION_CHOICES = (
	    (GOOD, 'Good'),
	    (RANDOM, 'Random'),
	    (MALICIOUS, 'Malicious'),
	)

	aws_worker_id = models.CharField(
	    _("Amazon worker id"), blank=True, max_length=255, null=True)
	bias = models.FloatField(_("bias"), default=0)
	uncertain_count = models.IntegerField(_("uncertainity count"), default=1)
	classification = models.CharField(
		_("Classification as GRM"),
	    choices=CLASSIFICATION_CHOICES,
	    default=None,
		max_length=1,
	    null=True
	)
	exit_bias = models.FloatField(_("Exit bias"), default=0)
	exit_round = models.IntegerField(_("Exit round"), null=True)

	def __str__(self):
	    return self.id.__str__()

	def get_hashid(self):
		return self.hashid.encode(self.id)

	def set_exit_classification_bias(self, bias, classification):
		'''to be used before save()'''
		self.exit_bias = bias
		self.classification = classification

	def set_exit_round(self, n):
		'''to be used before save()'''
		self.exit_round = n
		# self.save()

	def get_tasks(self):
		''' get tasks assigned to this user '''
	pass


pre_save.connect(upate_uncertain_count, sender=AmazonWorker)


class HIT(TimeStampedModel):
	"""
	Human Intelligence Task
	Tasks created on Amazon Mechanical Turk
	"""
	def __str__(self):
		return self.id.__str__() + ' ' + self.hit_id.__str__()

	GOOD = 'G'
	RANDOM = 'R'
	MALICIOUS = 'M'
	USER_CHOICES = (
	    (GOOD, 'Good'),
	    (RANDOM, 'Random'),
	    (MALICIOUS, 'Malicious'),
	)

	hit_id = models.CharField(
		_("Amazon HIT Id"), unique=True, null=True, max_length=255)
	url = models.CharField(_("url for hit"), default='', max_length=255, null=True)
	title = models.CharField(_("Title"), max_length=255, null=True)
	description = models.CharField(_("Description"), max_length=255, null=True)
	keywords = ArrayField(models.CharField(max_length=255, null=True))
	frame_height = models.IntegerField(default=500) # the height of the iframe holding the external hit
	amount = models.IntegerField(default=0.01)
	expected_bias = models.CharField(
	    _("Bias as per instruction"),
	    max_length=1,
	    choices=USER_CHOICES,
	    default=RANDOM
	)


class Assignment(TimeStampedModel):
	"""Assignment from Amazon"""
	def __str__(self):
		return self.id.__str__() + ' ' + self.assignment_id.__str__()

	assignment_id = models.CharField(
		_("Amazon Assignment Id"), null=True, max_length=255)
	user = models.ForeignKey(AmazonWorker)
	hit = models.ForeignKey(HIT)
	# accepted_time = self.created_time
	time_of_completion = models.DateTimeField(null=True)
	time_due_at = models.DateTimeField(null=True)
	url_turk_submission = models.CharField(null=True, max_length=255)
