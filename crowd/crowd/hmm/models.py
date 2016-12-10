# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import csv, random
import numpy as np

from pomegranate import *
from pomegranate import HiddenMarkovModel

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField

# from crowd.turk.models import AmazonWorker
from crowd.utilities.models import TimeStampedModel

class HMM(TimeStampedModel):
    """
    Hidden Markov Model
    """
    name = models.CharField(max_length=200, null=True)
    json_model = JSONField(null=True)
    states = ArrayField(models.FloatField(), null=True)
    gold_ratio = models.FloatField(null=True)


    def __unicode__(self):
        return self.id

    @property
    def _model(self):
        return HiddenMarkovModel.from_json(self.json_model)

    def new_gold_ratio(self, obsevation):
        '''
        calculate new gold ratio
        '''
        try:
            prediction = int(self._model.predict(obsevation)[0])
        except Exception as e:
            print e
            prediction = 8
        return self.calculate_gold(prediction)

    def calculate_gold(self, prediction):
        # y = -10/3*x + 7/3
        self.gold_ratio = (-10.0/3) * prediction + 7.0/4
        self.save()
        return self.gold_ratio

    def train(self, observations):
        '''
        trains the model and returns the new json
        '''
        model = self._model
        print model.fit(observations, algorithm='baum-welch', stop_threshold=1)
        return model.to_json()


    def get_new_emissions(self):
        # # Replace all -inf with 0
        # qwer = []
        # for tt in ems:
        #     m = []
        #     for t in tt:
        #         d = t
        #         if np.isinf(t):
        #             d = 0
        #         m += [d]
        #     qwer += [m]
        # ems = qwer

        # # convert to distribution
        # new_emissions = []
        # for row in ems:
        #     t = {}
        #     for (i, val) in enumerate(row):
        #         t[i] = float(val)
        #     new_emissions += [DiscreteDistribution(t)]
        # return new_emissions
        pass

    def get_new_transitions(self):
        # new_transitions = []
        # for row in trans:
        #     t = list(map(float, row))
        #     new_transitions += [t]
        # return np.array(new_transitions)
        pass

    def save_csv(self):
        """
        Save results into a csv
        """
        pass



# class Task(TimeStampedModel):
#   title = models.CharField(_("Title"), max_length=255)
#   question = models.CharField(_("Question"), max_length=1000)
#   answers = models.ManyToManyField('AnswerOption')


# class TaskAssignment(TimeStampedModel):
#   user = models.ForeignKey(AmazonWorker, related_name='task_assignments')
#   task = models.ForeignKey(Task, related_name='assignments')
#   user_answer = models.ForeignKey('AnswerOption', null=True)
#   user_answer_time = models.DateTimeField(null=True)
#   bias_at_answer = models.FloatField(_("bias"), default=0)
#   gradient_at_answer = models.FloatField(_("Gradient"), default = 0)

#   maximum = 10
#   middle = 0
#   minimum = -10
#   unbiased_increment = 1
#   stop_watermark_point_basis = 4
#   behaviour_percent = 0.15
#   anti_behaviour_percent = 0.2

#   def __str__(self):
#       return self.id.__str__()

#   def get_new_bias(self):
#       if self.user_answer.correct:
#           return self.new_bias_correct()
#       else:
#           return self.new_bias_incorrect()

#   def new_bias_correct(self):
#       print 'new_bias_correct'
#       old_bias = self.user.bias
#       if self.user.uncertain_count == 1:
#           # 1st uncertain region
#           return old_bias + self.unbiased_increment
#       if old_bias < -self.stop_watermark_point_basis:     # current negative bias
#           d1 = abs(-self.maximum - old_bias)
#           d2 = abs(self.middle - old_bias)
#           d = d1 if d1>=d2 else d2
#           return old_bias + self.anti_behaviour_percent*d
#       else:                                               # current positive bias
#           d = self.maximum - old_bias
#           return old_bias + self.behaviour_percent*d

#   def new_bias_incorrect(self):
#       print 'new_bias_incorrect'
#       old_bias = self.user.bias
#       if self.user.uncertain_count == 1:
#           return old_bias - self.unbiased_increment
#       if old_bias >  self.stop_watermark_point_basis:     # current positive bias
#           d1 = abs(self.maximum - old_bias)
#           d2 = abs(self.middle - old_bias)
#           d = d1 if d1>=d2 else d2
#           return old_bias - self.anti_behaviour_percent*d
#       else:                                               # current negative bias
#           d = self.maximum + old_bias
#           return old_bias - self.behaviour_percent*d

# post_save.connect(check_good_worker, sender=TaskAssignment)


# class AnswerOption(TimeStampedModel):
#   text = models.CharField(_("Answer option"), max_length=255)
#   correct = models.BooleanField(default=False)

#   def __str__(self):
#       return self.text
