import numpy
import datetime

from django.conf import settings

def check_good_worker(sender, instance, **kwargs):
    # from crowd.tasks.models import TaskAssignment as ta
    print '```````check_good_worker`````'

    # update_gradient(instance)
    try:
        task_assignments = instance.user.task_assignments.filter(
            user_answer_time__lte=instance.user_answer_time).exclude(
            user_answer=None).order_by('user_answer_time')
    except ValueError as e:
        print e
        return
    print 'task_assignments count=' + str(len(task_assignments))

    if len(task_assignments) < settings.GOOD_GRADIENT_BIAS_LENGTH or instance.user.uncertain_count < 2:
        # check length and uncertainty
        return

    diff = []
    tas = list(task_assignments.reverse()[:4])
    print tas
    for ta in tas:
        index = tas.index(ta)
        try:
            diff += [(tas[index].gradient_at_answer - tas[index+1].gradient_at_answer)/tas[index+1].gradient_at_answer]
        except IndexError as e:
            print e
        except ZeroDivisionError as e:
            print e
            diff += [0]
    print diff
    high = max(diff)
    low = min(diff)
    if (high - low) < settings.GOOD_GRADIENT_DELTA_BIAS:
        # exit loop, good user
        print 'good user'
        worker = instance.user
        if worker.exit_round == 0.0:
            worker.set_exit_classification_bias(worker.bias, worker.GOOD)
            exit_round = list(task_assignments).index(instance)
            print exit_round
            # if worker.exit_round > exit_round:
            worker.set_exit_round(exit_round)
            worker.save()
