import datetime
from dateutil import parser
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

def queryset_filter(queryset, task_list=None,
                    startdate=None, enddate=None, user_list=None):
    if startdate is not None:
        if type(startdate) not in (datetime.date, datetime.datetime):
            try:
                startdate = parser.parse(startdate).date()
                queryset = queryset.filter(date__gte=startdate)
            except:
                pass
    if enddate is not None:
        if type(enddate) not in (datetime.date, datetime.datetime):
            try:
                enddate = parser.parse(enddate).date()
                queryset = queryset.filter(date__lte=enddate)
            except:
                pass
    if task_list is not None:
        queryset = queryset.filter(task__in=task_list)
    if user_list is not None:
        queryset = queryset.filter(profile__in=user_list)
    return queryset

def sum_and_sort_time(queryset, limit=None):
    queryset = queryset.values('task__name').order_by('task__name'
                    ).annotate(Sum('duration')).order_by('duration__sum'
                    ).reverse()
    if limit is not None:
        queryset = queryset[:limit]
    return queryset

def resources_involved(queryset, limit=None):
    queryset = queryset.distinct('profile', 'task')
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
    queryset = queryset.distinct('profile')
    return queryset.count()
