import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backapps.salary.models import DailySalary
from backapps.record.models import (Record, DailyDataPerTaskPerUser,
                                    DailyDataPerTask)
from libs.chart.calculus import record2daily
from django.db.models import Sum

@receiver(post_save, sender=Record)
#def update_DailyDurationPerTaskPerUser(sender, instance, *args, **kwargs):
def on_record_change(sender, instance, *args, **kwargs):
    (workspace, task, profile) = (instance.workspace, instance.task,
                                  instance.profile)
    if instance.start and instance.end:
        start = instance.start.replace(hour=0, minute=0,
                                         second=0, microsecond=0)
        end = instance.end.replace(hour=0, minute=0, second=0, microsecond=0)
        end += datetime.timedelta(1)
        # get all records from the same period for the same task & same user
        qs = Record.objects.by_workspace(workspace).filter(
                                            start__gte=start, end__lte=end,
                                            task=task, profile=profile)
        # calculate durations per day per task per user
        data_dict = record2daily(qs)
        #data_dict = record2daily(instance)
        for date in data_dict.iterkeys():
            (ddtu, created) = DailyDataPerTaskPerUser.objects.get_or_create(
                                workspace=workspace,
                                task=task, date=date, profile=profile)
            ddtu.duration = data_dict[date].total_seconds()/3600
            ddtu.save()
        # calculate costs per day per task per user
        for date in data_dict.iterkeys():
            daily_user_tasks = DailyDataPerTaskPerUser.objects.by_workspace(
                                workspace).filter(profile=profile, date=date)
            duration_sum = daily_user_tasks.aggregate(Sum('duration')
                                                            )['duration__sum']
            if duration_sum != 0:
                daily_wage = 0
                try:
                    daily_wage = DailySalary.objects.by_workspace(workspace).get(
                                        profile=profile,
                                        start_date__lte=date, end_date__gte=date
                                        ).daily_wage
                except DailySalary.DoesNotExist:
                    pass
                ### !!! except more than one
                    ### mistake somewhere
                for i in daily_user_tasks:
                    i.ratio = i.duration / duration_sum
                    i.wage = daily_wage
                    i.cost = i.ratio * i.wage
                    i.save()
        # calculate duration per day per task, incl. its descendants
        for date in data_dict.iterkeys():
            daily_task_data = DailyDataPerTaskPerUser.objects.by_workspace(
                                workspace).filter(date=date, task=task)
            daily_duration = daily_task_data.aggregate(Sum('duration')
                                                            )['duration__sum']
            daily_cost = daily_task_data.aggregate(Sum('cost')
                                                            )['cost__sum']
            sub_tasks = task.get_children()
            children_duration = 0
            children_cost = 0
            for s in sub_tasks:
                children_data = DailyDataPerTask.objects.by_workspace(
                                        workspace).filter(date=date,
                                                          task__in=sub_tasks)
                if len(children_data) > 0:
                    children_duration += children_data.aggregate(
                                            Sum('duration'))['duration__sum']
                    children_cost += children_data.aggregate(
                                            Sum('cost'))['cost__sum']
            total_duration = daily_duration + children_duration
            total_cost = daily_cost + children_cost
            (ddt, created) = DailyDataPerTask.objects.get_or_create(date=date,
                                    workspace=workspace, task=task)
            diff_duration = total_duration - ddt.duration
            diff_cost =  total_cost - ddt.cost
            ddt.duration = total_duration
            ddt.cost = total_cost
            ddt.save()
            for a in task.get_ancestors():
                (ddt, created) = DailyDataPerTask.objects.get_or_create(
                                                        date=date, task=a,
                                                        workspace=workspace)
                ddt.duration += diff_duration
                ddt.cost += diff_cost
                ddt.save()

#post_save.connect(update_DailyDurationPerTaskPerUser, sender=Record)

#@receiver(post_save, sender=DailyDurationPerTaskPerUser)
#@receiver(post_save, sender=DailySalary)
#def update_DailyCostPerTaskPerUser(sender, instance, created, *args, **kwargs):
    #workspace = instance.workspace
    #profile   = instance.profile
    #if sender == DailyDurationPerTaskPerUser:
        #if created:
            #DailyCostPerTaskPerUser.objects.create(workspace=workspace,
                                                   #ddtu=instance)
        #date = instance.date
        #daily_tasks = DailyDurationPerTaskPerUser.objects.by_workspace(
                            #workspace).filter(profile=profile, date=date)
        #duration_sum = daily_tasks.aggregate(Sum('duration'))['duration__sum']
        #if duration_sum != 0:
            #daily_wage = 0
            #try:
                #daily_wage = DailySalary.objects.by_workspace(workspace).get(
                                    #profile=profile,
                                    #start_date__lte=date, end_date__gte=date
                                    #).daily_wage
            #except DailySalary.DoesNotExist:
                #pass
            #### !!! except more than one
                #### mistake somewhere
            #for i in daily_tasks:
                #dctu = i.dailycostpertaskperuser
                #dctu.time_percent = i.duration / duration_sum
                #dctu.wage = daily_wage
                #dctu.cost = dctu.time_percent * dctu.wage
                #dctu.save()
    #elif sender == DailySalary:
        #start_date = instance.start_date
        #end_date   = instance.end_date
        #new_wage   = instance.daily_wage
        #daily_tasks = DailyDurationPerTaskPerUser.objects.by_workspace(
                            #workspace).filter(profile=profile,
                                              #date__gte=start_date,
                                              #date__lte=end_date)
        #for i in daily_tasks:
            #dctu = i.dailycostpertaskperuser
            #dctu.wage = new_wage
            #dctu.cost = dctu.time_percent * dctu.wage
            #dctu.save()

##post_save.connect(update_DailyCostPerTaskPerUser,
                  ##sender=DailyDurationPerTaskPerUser)
##post_save.connect(update_DailyCostPerTaskPerUser,
                  ##sender=DailySalary)

#@receiver(post_save, sender=DailyDurationPerTaskPerUser)
#def update_DailyDurationPerTask(sender, instance, *args, **kwargs):
    #workspace = instance.workspace
    #task      = instance.task
    #date      = instance.date
    ##duration_sum = DailyDurationPerTaskPerUser.objects.filter(
                            ##task=task, date=date
                            ##).aggregate(Sum('duration'))['duration__sum']
    #(ddt, created) = DailyDurationPerTask.objects.get_or_create(
                                #workspace=workspace,
                                #task=task, date=date)
    ##ddt.duration = duration_sum
    #ddt.duration += instance.duration
    #ddt.save()

##post_save.connect(update_DailyDurationPerTask,
                  ##sender=DailyDurationPerTaskPerUser)

#@receiver(post_save, sender=DailyCostPerTaskPerUser)
#def update_DailyCostPerTask(sender, instance, *args, **kwargs):
    #workspace = instance.workspace
    #task      = instance.ddtu.task
    #date      = instance.ddtu.date
    ##cost_sum = DailyCostPerTaskPerUser.objects.filter(
                            ##ddtu__task=task, ddtu__date=date
                            ##).aggregate(Sum('cost'))['cost__sum']
    #(dct, created) = DailyCostPerTask.objects.get_or_create(
                                #workspace=workspace,
                                #task=task, date=date)
    ##dct.cost = cost_sum
    #dct.cost += instance.cost
    #dct.save()

##post_save.connect(update_DailyCostPerTask,
                  ##sender=DailyCostPerTaskPerUser)

##def update_DailyCostPerHierarchy(sender, instance, *args, **kwargs):
    ##workspace = instance.workspace
    ##task      = instance.task
    ##date      = instance.date
    ##cost_sum = DailyCostPerTaskPerUser.objects.filter(
                            ##ddtu__task=task, ddtu__date=date
                            ##).aggregate(Sum('cost'))['cost__sum']
    ##(dct, created) = DailyCostPerHierarchy.objects.get_or_create(
                                ##workspace=workspace,
                                ##task=task, date=date)
    ##dct.cost = cost_sum
    ##dct.save()

##post_save.connect(update_DailyCostPerHierarchy,
                  ##sender=DailyCostPerTask)

