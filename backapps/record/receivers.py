import datetime
from decimal import Decimal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backapps.task.models import Task, parent_changed
from backapps.salary.models import DailySalary
from backapps.record.models import (AutoRecord, DailyDataPerTaskPerUser,
                                    DailyDataPerTask)
from libs.chart.calculus import record2daily
from django.db.models import Sum

@receiver(post_save, sender=AutoRecord)
def on_record_change(sender, instance, *args, **kwargs):
    (workspace, profile) = (instance.workspace, instance.profile)
    if instance.start and instance.end:
        # calculate durations per day (record might last several days)
        data_dict = record2daily(instance)
        # for each date update ddtu
        for date in data_dict.iterkeys():
            record_duration = data_dict[date].total_seconds()/3600
            # skip records smaller than 36 seconds
            if record_duration < 0.01:
                continue
            (ddtu, created) = DailyDataPerTaskPerUser.objects.get_or_create(
                                                workspace=workspace,
                                                task=instance.task,
                                                date=date, profile=profile)
            ddtu.duration += Decimal(record_duration)
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
                i.ratio = i.duration / duration_sum
                i.cost = i.ratio * i.wage
                i.save()
                
@receiver(pre_save, sender=DailyDataPerTaskPerUser)
def on_ddtu_change(sender, instance, *args, **kwargs):
    # get last data, get new data, calculate diff
    if instance.id:
        prev = DailyDataPerTaskPerUser.objects.get(pk=instance.id)
        prev_duration = prev.duration
        prev_cost = prev.cost
    else:
        prev_duration = 0
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
            my_duration = 0
            my_cost = 0
        # save
        instance.duration = my_duration + instance.children_duration
        instance.cost = my_cost + instance.children_cost
        instance.save()

@receiver(post_save, sender=DailySalary)
def on_salary_change(sender, instance, *args, **kwargs):
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
    workspace = instance.workspace
    # if parent changed
    if prev_parent != new_parent:
        # remove data from parent
        ancestors = instance.get_ancestors()
        parents = DailyDataPerTask.objects.filter(task__in=ancestors,
                                                  workspace=workspace)
        for parent in parents:
            child = DailyDataPerTask.objects.get(task=instance,
                                                 date=parent.date,
                                                 workspace=workspace)
            parent.duration -= child.duration
            parent.cost -= child.cost
            parent.save()
        # add data to new parent
        parents = DailyDataPerTask.objects.filter(task=new_parent,
                                                  workspace=workspace)
        for parent in parents:
            child = DailyDataPerTask.objects.get(task=instance,
                                                 date=parent.date,
                                                 workspace=workspace)
            parent.duration += child.duration
            parent.cost += child.cost
            parent.save()
