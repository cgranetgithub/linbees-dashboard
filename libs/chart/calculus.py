import datetime
from operator import itemgetter
from django.db.models import Sum, Count
from collections import defaultdict, OrderedDict

def record2daily(queryset):
    one_day = datetime.timedelta(1)
    date_dict = defaultdict(datetime.timedelta)
    for record in queryset:
        if record.end() is not None:
            start_date = record.start().date()
            end_date = record.end().date()
            if start_date > end_date:
                    raise Exception("error start_date > end_date")
            #same day
            elif start_date == end_date:
                duration = record.end() - record.start()
                date_dict[start_date] += duration
            #several days
            else: # start < end
                iter_date = start_date
                #first day
                duration = datetime.datetime(
                                iter_date.year, iter_date.month, iter_date.day
                            , tzinfo=record.start().tzinfo
                        ) + one_day - record.start()
                date_dict[iter_date] += duration
                iter_date += one_day
                #days in the middle
                while iter_date < end_date:
                    date_dict[iter_date] += one_day
                    iter_date += one_day
                #last day
                duration = record.end() - datetime.datetime(
                                    iter_date.year, iter_date.month
                                , iter_date.day, tzinfo=record.end().tzinfo)
                date_dict[iter_date] += duration
    data_dict = OrderedDict(sorted(date_dict.items(), key=lambda t: t[0]))
    return data_dict

def queryset_filter(queryset, task_list=None, user_list=None,
                        startdate=None, enddate=None):
    if startdate:
        queryset = queryset.filter(date__gte=startdate)
    if enddate:
        queryset = queryset.filter(date__lte=enddate)
    if task_list:
        queryset = queryset.filter(task__in=task_list)
    if user_list:
        queryset = queryset.filter(user__in=user_list)
    return queryset

def sum_and_sort_time(queryset, limit=None):
    queryset = queryset.values('task__name').order_by('task__name'
                    ).annotate(Sum('duration')).order_by('duration__sum'
                    ).reverse()
    if limit is not None:
        queryset = queryset[:limit]
    return queryset

def resources_involved(queryset, limit=None):
    queryset = queryset.distinct('user', 'task')
    data = defaultdict(int)
    for i in queryset:
        data[i.task] += 1
    result = OrderedDict(sorted(data.items(), key=lambda t: t[1]))
    items = result.items()
    items.reverse()
    if limit is not None:
        items = items[:limit]
    return items

def active_users(queryset):
    queryset = queryset.distinct('user')
    return queryset.count()

#def records2days(queryset):
    #one_day = datetime.timedelta(1)
    #date_dict = defaultdict(defaultdict)
    #for record in queryset:
        ##task_set.add(record.task)
        #if record.end() is not None:
            #start_date = record.start().date()
            #end_date = record.end().date()
            #if start_date not in date_dict:
                #date_dict[start_date] = defaultdict(datetime.timedelta)
            #if end_date not in date_dict:
                #date_dict[end_date] = defaultdict(datetime.timedelta)
            ##same day
            #if start_date == end_date:
                #duration = record.end() - record.start()
                #date_dict[start_date][record.task] += duration
            ##several days
            #else:
                #iter_date = start_date
                ##first day
                #duration = datetime.datetime(iter_date.year, iter_date.month
                                            #, iter_date.day
                                            #, tzinfo=record.start().tzinfo) + one_day - record.start()
                #date_dict[iter_date][record.task] += duration
                ##days in the middle
                #while iter_date != end_date:
                    #duration = datetime.timedelta(1)
                    #if iter_date not in date_dict:
                        #date_dict[iter_date] = defaultdict(datetime.timedelta)
                    #date_dict[iter_date][record.task] += duration
                    #iter_date += one_day
                ##last day
                #duration = record.end() - datetime.datetime(iter_date.year, iter_date.month
                                                    #, iter_date.day
                                                    #, tzinfo=record.end().tzinfo)
                #date_dict[iter_date][record.task] += duration
    #data_dict = OrderedDict(sorted(date_dict.items(), key=lambda t: t[0]))
    #return data_dict

#def tasksAlongTime2(workspace, task_id=None):
    #t = datetime.datetime.now()
    #if task_id is not None:
        #qs = Record.objects.by_workspace(workspace).filter(task__id=task_id)
        #tasks = [Task.objects.by_workspace(workspace).get(pk=task_id)]
    #else:
        #qs = Record.objects.by_workspace(workspace).all()
        #p_dicts = Record.objects.by_workspace(workspace).values("task")
        #p_list = [p["task"] for p in p_dicts]
        #tasks = [Task.objects.by_workspace(workspace).get(pk=p) for p in set(p_list)]
    #if qs.count() == 0:
        #return ({}, [])
    #data_dict = records2days(qs)
    #return (data_dict, tasks)

#def cumulate(data_dict, task_list):
    #if data_dict == {}:
        #return {}
    #cum_dict = defaultdict(defaultdict)
    #dates = data_dict.keys()
    #prev_date = dates[0]
    #cum_dict[prev_date] = data_dict[prev_date]
    #for date in dates[1:]:
        #cum_dict[date] = defaultdict(datetime.timedelta)
        #for p in task_list:
            #cum_dict[date][p] = cum_dict[prev_date][p] + data_dict[date][p]
        #prev_date = date
    #ret_dict = OrderedDict(sorted(cum_dict.items(), key=lambda t: t[0]))
    #return ret_dict

#def tasksSum(workspace):
    #tasks = Task.objects.by_workspace(workspace).all()
    #time_dict = defaultdict(datetime.timedelta)
    #for p in tasks:
        #records = Record.objects.by_workspace(workspace).filter(task__name__exact=p.name)
        #sum_time = datetime.timedelta(0)
        #for r in records:
                #if r.end() is not None:
                        #sum_time += r.end() - r.start()
        #time_dict[p] = sum_time
    #return time_dict
