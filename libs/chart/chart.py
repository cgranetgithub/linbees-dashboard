import datetime
from django.db.models import Sum
#from libs.chart.calculus import cumulate, groupByMonth, groupByYear
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
                        ).values_list('task_id').distinct('task__id')
    tasks = Task.for_tenant(workspace
                            ).objects.filter(id__in=id_list).order_by('name')
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

#def users_over_time(workspace, user):
    #if user is None:
        #return ([], {})
    #queryset = DailyRecord.for_tenant(workspace).objects.filter(user=user
                                                            #, task__monitored=True)
    ## get dates (warning works only with postegresql because of distinct)
    #dates = queryset.values_list('date', flat=True).order_by('date').distinct('date')
    ## get tasks (no distinct on foreignkey for now in django)
    #id_list = queryset.order_by('task__name').values_list('task_id'
                                                            #).distinct('task__id')
    #tasks = Task.for_tenant(workspace).objects.filter(id__in=id_list
                                                        #, monitored=True)
    ## build array
    #array = [['Dates'] + [ p.name.encode('latin1') for p in tasks] ]
    #for d in dates:
        #tmp = [d.isoformat()]
        #for p in tasks:
            #try:
                #duration = queryset.get(date=d, task=p.id).duration
            #except DailyRecord.DoesNotExist:
                #tmp.append(0)
            #else:
                #tmp.append(float(duration))
        #array.append(tmp)
    #options = { 'title':'User task', 'is3D':'true'
                #, 'backgroundColor':'transparent', 'isStacked':'true'
                #};
    #return (array, options)

def cumulative_task_over_time(array):
    # start from 1: to skip title row / col
    cum_array = []
    if len(array) > 1:
        previous = array[1][1:]
        cum_array = [array[0], array[1]]
        for i in array[2:]:
            tmp = [x+y for (x,y) in zip(previous, i[1:])]
            cum_array.append([i[0]] + tmp)
            previous = tmp
    cum_options = {'is3D':'true', 'backgroundColor':'transparent'}
    return (cum_array, cum_options)

#def bar(data_dict, task_list):
    #if len(data_dict) > 40:
        #data = groupByMonth(data_dict)
    #elif len(data_dict) > 1200:
        #data = groupByYear(data_dict)
    #else:
        #data = data_dict
    #bar_data = [['Date'] + [str(p.name) for p in task_list]]
    #for d in data:
        #if isinstance(d, datetime.date):
            #tmp = [d.isoformat()]
        #else:
            #tmp = ["-".join(d)]
        #for p in task_list:
            #if p in data[d]:
                #duration = data[d][p].total_seconds() / 3600
            #else:
                #duration = 0
            #tmp.append(duration)
        #if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
            #bar_data.append(tmp)
    #bar_options = { 'title':'Tasks evolution', 'is3D':'true'
                #, 'backgroundColor':'transparent', 'isStacked':'true'
                #};
    #return (bar_data, bar_options)

#def line(data_dict, task_list):
    #line_data = [['Date'] + [str(p.name) for p in task_list]]
    #for d in data_dict:
        #tmp = [d.isoformat()]
        #for p in task_list:
            #if p in data_dict[d]:
                #duration = data_dict[d][p].total_seconds() / 3600
            #else:
                #duration = 0
            #tmp.append(duration)
        #if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
            #line_data.append(tmp)
    #line_options = {'title':'Tasks evolution', 'is3D':'true', 'backgroundColor':'transparent'}
    #return (line_data, line_options)

#def line_cumulate(data_dict, task_list):
    #cum_dict = cumulate(data_dict, task_list)
    #cum_data = [['Date'] + [str(p.name) for p in task_list]]
    #for d in cum_dict:
        #tmp = [d.isoformat()]
        #for p in task_list:
            #if p in cum_dict[d]:
                #duration = cum_dict[d][p].total_seconds() / 3600
            #else:
                #duration = 0
            #tmp.append(duration)
        #if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
            #cum_data.append(tmp)
    #cum_options = { 'title':'Tasks evolution (cumulative)', 'is3D':'true'
                #, 'backgroundColor':'transparent'
                #}
    #return (cum_data, cum_options)
        