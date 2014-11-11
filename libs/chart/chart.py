import datetime
from django.db.models import Sum
from libs.chart.calculus import sum_and_sort_time, queryset_filter
from backapps.record.models import DailyRecord
from backapps.task.models import Task

def pie_total_time(queryset):
    queryset = sum_and_sort_time(queryset)
    data_list = [ [ (i['task__name']).encode('latin1')
                ,int(i['duration__sum'])               ] for i in queryset ]
    pie_data = [['Task', 'total time (hours)']] + data_list
    pie_options = {'is3D':'true', 'backgroundColor':'transparent'};
    return (pie_data, pie_options)

def tasks_over_time(workspace, queryset):
    # get dates (warning works only with postegresql because of distinct)
    dates = queryset.values_list('date', flat=True).order_by('date'
                                                            ).distinct('date')
    # get tasks
    id_list = queryset.order_by('task__name'
                        ).values_list('task_id').distinct('task__name')
    tasks = Task.objects.by_workspace(workspace
                            ).filter(id__in=id_list).order_by('name')
    # build array
    array = [['Dates'] + [ p.name.encode('latin1') for p in tasks] ]
    for d in dates:
        tmp = [d.isoformat()]
        for p in tasks:
            try:
                duration = queryset.filter(date=d, task=p).aggregate(
                                            Sum('duration'))['duration__sum']
            except DailyRecord.DoesNotExist:
                tmp.append(0)
            else:
                tmp.append(int(duration or 0))
        array.append(tmp)
    options = {'is3D':'true', 'backgroundColor':'transparent'}
    return (array, options)

### DIRTY this should be reworked ###
def cumulative_task_over_time(array, startdate=None, enddate=None):
    # start from 1: to skip title row / col
    cum_array = []
    if len(array) > 1:
        cum_array.insert(0, array[1])
        previous = array[1][1:]
        for i in array[2:]:
            tmp = [x+y for (x,y) in zip(previous, i[1:])]
            cum_array.append([i[0]] + tmp)
            previous = tmp
    cum_options = {'is3D':'true', 'backgroundColor':'transparent'}
    startindex = 0
    endindex = len(cum_array)
    if startdate and enddate:
        for i in cum_array:
            if startdate.isoformat() == i[0]:
                startindex = cum_array.index(i)
            if enddate.isoformat() == i[0]:
                endindex = cum_array.index(i)
        cum_array = cum_array[startindex:endindex+1]
    cum_array.insert(0, array[0])
    return (cum_array, cum_options)
