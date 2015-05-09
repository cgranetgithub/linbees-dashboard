import datetime
from decimal import Decimal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from task.models import Task, parent_changed
from salary.models import DailySalary
from record.models import (AutoRecord, DailyDataPerTaskPerUser,
                                    DailyDataPerTask)
from libs.chart.calculus import record2daily
import datetime
from django.db.models import Sum

import logging
logger = logging.getLogger('django')

@receiver(post_save, sender=AutoRecord)
def on_record_change(sender, instance, *args, **kwargs):
    if instance.start and instance.end:
        logger.debug("on_record_change %s %s"%(sender, instance))
        (workspace, profile) = (instance.workspace, instance.profile)
        # calculate durations per day (record might last several days)
        data_dict = record2daily(instance)
        # for each date update ddtu
        for date in data_dict.iterkeys():
            record_duration = data_dict[date]
            # skip records smaller than x seconds
            if record_duration < datetime.timedelta(seconds=5):
                continue
            (ddtu, created) = DailyDataPerTaskPerUser.objects.get_or_create(
                                                workspace=workspace,
                                                task=instance.task,
                                                date=date, profile=profile)
            ddtu.duration += record_duration
            if created:
                daily_wage = 0
                try:
                    daily_wage = DailySalary.objects.get(
                                            profile=profile,
                                            start_date__lte=date,
                                            end_date__gte=date,
                                            workspace=workspace).daily_wage
                except DailySalary.DoesNotExist:
                    pass
                ### !!! except more than one
                    ### mistake somewhere
                ddtu.wage = daily_wage
            ddtu.save()
            # calculate costs
            ddtu_list = DailyDataPerTaskPerUser.objects.filter(
                                                profile=profile, date=date,
                                                workspace=workspace)
            duration_sum = ddtu_list.aggregate(Sum('duration')
                                                            )['duration__sum']
            for i in ddtu_list:
                i.time_ratio = Decimal( i.duration.total_seconds() / 
                                              duration_sum.total_seconds() )
                i.cost = i.time_ratio * i.wage
                i.save()
                
@receiver(pre_save, sender=DailyDataPerTaskPerUser)
def on_ddtu_change(sender, instance, *args, **kwargs):
    logger.debug("on_ddtu_change %s %s"%(sender, instance))
    # get last data, get new data, calculate diff
    if instance.id:
        prev = DailyDataPerTaskPerUser.objects.get(pk=instance.id)
        prev_duration = prev.duration
        prev_cost = prev.cost
    else:
        prev_duration = datetime.timedelta(0)
        prev_cost = 0
    duration_diff = instance.duration - prev_duration
    cost_diff = instance.cost - prev_cost
    # get corresponding ddt + ancestors and add diff
    task_list = instance.task.get_ancestors(include_self=True)
    for t in task_list:
        (ddt, created) = DailyDataPerTask.objects.get_or_create(
                                                workspace=instance.workspace,
                                                date=instance.date, task=t)
        ddt.duration += duration_diff
        ddt.cost += cost_diff
        if t != instance.task:
            ddt.children_duration += duration_diff
            ddt.children_cost += cost_diff
        ddt.save()
    
@receiver(post_save, sender=DailyDataPerTask)
def on_ddt_creation(sender, instance, created, *args, **kwargs):
    # if new, calculate children data & self data
    if created:
        logger.debug("on_ddt_creation %s %s"%(sender, instance))
        workspace = instance.workspace
        # children
        children_tasks = instance.task.get_children()
        children = DailyDataPerTask.objects.filter(date=instance.date,
                                                   task__in=children_tasks,
                                                   workspace=workspace)
        if len(children) > 0:
            instance.children_duration = children.aggregate(Sum('duration')
                                                            )['duration__sum']
            instance.children_cost = children.aggregate(Sum('cost')
                                                            )['cost__sum']
        # self
        ddtu_list = DailyDataPerTaskPerUser.objects.filter(date=instance.date,
                                                           task=instance.task,
                                                           workspace=workspace)
        if len(ddtu_list) > 0 :
            my_duration = ddtu_list.aggregate(Sum('duration'))['duration__sum']
            my_cost = ddtu_list.aggregate(Sum('cost'))['cost__sum']
        else:
            my_duration = datetime.timedelta(0)
            my_cost = 0
        # save
        instance.duration = my_duration + instance.children_duration
        instance.cost = my_cost + instance.children_cost
        instance.save()

@receiver(post_save, sender=DailySalary)
def on_salary_change(sender, instance, *args, **kwargs):
    logger.debug("on_salary_change %s %s"%(sender, instance))
    # update ddtu with new wage
    ddtu_list = DailyDataPerTaskPerUser.objects.filter(
                                            profile=instance.profile,
                                            date__gte=instance.start_date,
                                            date__lte=instance.end_date,
                                            workspace=instance.workspace)
    for i in ddtu_list:
        i.wage = instance.daily_wage
        i.cost = i.time_ratio * i.wage
        i.save()

@receiver(parent_changed, sender=Task)
def on_task_parent_change(sender, instance, prev_parent, new_parent, **kwargs):
    # if parent changed
    if prev_parent != new_parent:
        logger.debug("on_task_parent_change %s %s %s"%(instance, prev_parent,
                                                      new_parent))
        workspace = instance.workspace
        if prev_parent:
            # get all ancestors tasks starting from previous parent
            ancestors = prev_parent.get_ancestors(include_self=True)
            # get all ddt which are ancestors
            parents = DailyDataPerTask.objects.filter(task__in=ancestors,
                                                    workspace=workspace)
            for parent in parents:
                # get instance for the same date as parent
                child = DailyDataPerTask.objects.get(task=instance,
                                                    date=parent.date,
                                                    workspace=workspace)
                # remove duration and cost
                parent.duration -= child.duration
                parent.children_duration -= child.duration
                parent.cost -= child.cost
                parent.children_cost -= child.cost
                parent.save()
        if new_parent:
            # get all ancestors tasks starting from new parent
            ancestors = new_parent.get_ancestors(include_self=True)
            # get all ddt which are ancestors
            parents = DailyDataPerTask.objects.filter(task__in=ancestors,
                                                    workspace=workspace)
            for parent in parents:
                # get instance for the same date as parent
                child = DailyDataPerTask.objects.get(task=instance,
                                                    date=parent.date,
                                                    workspace=workspace)
                # add duration and cost
                parent.duration += child.duration
                parent.children_duration += child.duration
                parent.cost += child.cost
                parent.children_cost += child.cost
                parent.save()
