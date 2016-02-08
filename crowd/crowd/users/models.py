# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    # name = models.CharField(_("Name of User"), blank=True, max_length=255)


    def __str__(self):
    	return self.id.__str__()


class AmazonWorker(models.Model):
	"""Worker from Amazon"""
	
	# user = models.ForeignField(User)	
	aws_worker_id = models.CharField(
	    _("Amazon worker id"), blank=True, max_length=255)
	aws_key = models.CharField(
	    _("Amazon worker key"), unique=True, null=True, max_length=255)

	GOOD = 'G'
	RANDOM = 'R'
	MALICIOUS = 'M'
	USER_CHOICES = (
	    (GOOD, 'Good'),
	    (RANDOM, 'Random'),
	    (MALICIOUS, 'Malicious'),
	)
	expected_bias = models.CharField(
	    _("Bias as per instruction"),
	    max_length=1,
	    choices=USER_CHOICES,
	    default=RANDOM
	)
	bias = models.IntegerField(_("bias"), default=0)

	uncertain_count = models.IntegerField(_("uncertainity count"), default=0)

	def __str__(self):
	    return self.id.__str__()

	# def get_absolute_url(self):
	#     return reverse('users:detail', kwargs={'username': self.username})
