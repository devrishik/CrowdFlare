# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from crowd.utilities.models import TimeStampedModel


class task(TimeStampedModel):
	title = models.CharField(_("Title"), max_length=255)
	question = models.CharField(_("Question"), max_length=1000)
	answer_1 = models.CharField(_("Answer option 1"), max_length=255)
	answer_2 = models.CharField(_("Answer option 2"), max_length=255)
	correct_answer = models.CharField(_("Correct answer"), max_length=255)
	time_answered = models.DateTimeField(_("Time of answer"), null=True)
