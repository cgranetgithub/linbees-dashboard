import datetime
from django.db.models import Sum
#from libs.chart.calculus import cumulate, groupByMonth, groupByYear
from backapps.record.models import DailyRecord
from backapps.activity.models import Activity

def activities_total_time(workspace, activity_list=None, user_list=None):
    queryset = DailyRecord.for_tenant(workspace
			).objects.filter(activity__monitored=True)
    if activity_list:
	queryset = queryset.filter(activity__in=activity_list)
    if user_list:
	queryset = queryset.filter(user__in=user_list)
    queryset = queryset.values('activity__name'
			).order_by('activity__name').annotate(Sum('duration'))
    #if activity_list:
	#queryset = DailyRecord.for_tenant(workspace
			    #).objects.filter(activity__in=activity_list
					   #, activity__monitored=True
			    #).values('activity__name'
			    #).order_by('activity__name').annotate(Sum('duration'))
    #else:  
	#queryset = DailyRecord.for_tenant(workspace
			    #).objects.filter(activity__monitored=True
			    #).values('activity__name'
			    #).order_by('activity__name').annotate(Sum('duration'))
    data_list = [ [(i['activity__name']).encode('latin1'), float(i['duration__sum'])] for i in queryset ]
    pie_data = [['Activity', 'total time (hours)']] + data_list
    pie_options = {'title':'Activities distribution'
		   , 'is3D':'true'
		   , 'backgroundColor':'transparent'};
    return (pie_data, pie_options)

def activities_over_time(workspace, activity_list=None, user_list=None):
    queryset = DailyRecord.for_tenant(workspace
			).objects.filter(activity__monitored=True)
    if activity_list:
	queryset = queryset.filter(activity__in=activity_list)
    if user_list:
	queryset = queryset.filter(user__in=user_list)
    # get dates (warning works only with postegresql because of distinct)
    dates = queryset.values_list('date', flat=True).order_by('date').distinct('date')
    # get activities
    id_list = queryset.order_by('activity__name').values_list('activity_id').distinct('activity__id')
    activities = Activity.for_tenant(workspace).objects.filter(id__in=id_list)
    # build array
    array = [['Dates'] + [ p.name.encode('latin1') for p in activities] ]
    for d in dates:
	tmp = [d.isoformat()]
	for p in activities:
	    try:
		duration = queryset.filter(date=d, activity=p).aggregate(
					      Sum('duration'))['duration__sum']
	    except DailyRecord.DoesNotExist:
		tmp.append(0)
	    else:
		tmp.append(float(duration or 0))
	array.append(tmp)
    options = { 'title':'Activities evolution', 'is3D':'true'
		  , 'backgroundColor':'transparent'
		  };
    return (array, options)

def users_over_time(workspace, user):
    if user is None:
	return ([], {})
    queryset = DailyRecord.for_tenant(workspace).objects.filter(user=user
							      , activity__monitored=True)
    # get dates (warning works only with postegresql because of distinct)
    dates = queryset.values_list('date', flat=True).order_by('date').distinct('date')
    # get activities (no distinct on foreignkey for now in django)
    id_list = queryset.order_by('activity__name').values_list('activity_id'
							     ).distinct('activity__id')
    activities = Activity.for_tenant(workspace).objects.filter(id__in=id_list
							  , monitored=True)
    # build array
    array = [['Dates'] + [ p.name.encode('latin1') for p in activities] ]
    for d in dates:
	tmp = [d.isoformat()]
	for p in activities:
	    try:
		duration = queryset.get(date=d, activity=p.id).duration
	    except DailyRecord.DoesNotExist:
		tmp.append(0)
	    else:
		tmp.append(float(duration))
	array.append(tmp)
    options = { 'title':'User activity', 'is3D':'true'
		  , 'backgroundColor':'transparent', 'isStacked':'true'
		  };
    return (array, options)

def cumulative_activity_over_time(array):
    # start from 1: to skip title row / col
    cum_array = []
    if len(array) > 1:
	previous = array[1][1:]
	cum_array = [array[0], array[1]]
	for i in array[2:]:
	    tmp = [x+y for (x,y) in zip(previous, i[1:])]
	    cum_array.append([i[0]] + tmp)
	    previous = tmp
    cum_options = { 'title':'Activities evolution (cumulative)', 'is3D':'true'
		, 'backgroundColor':'transparent'
		}
    return (cum_array, cum_options)

#def bar(data_dict, activity_list):
    #if len(data_dict) > 40:
	#data = groupByMonth(data_dict)
    #elif len(data_dict) > 1200:
	#data = groupByYear(data_dict)
    #else:
	#data = data_dict
    #bar_data = [['Date'] + [str(p.name) for p in activity_list]]
    #for d in data:
	#if isinstance(d, datetime.date):
	    #tmp = [d.isoformat()]
	#else:
	    #tmp = ["-".join(d)]
	#for p in activity_list:
	    #if p in data[d]:
		#duration = data[d][p].total_seconds() / 3600
	    #else:
		#duration = 0
	    #tmp.append(duration)
	#if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
	      #bar_data.append(tmp)
    #bar_options = { 'title':'Activities evolution', 'is3D':'true'
		  #, 'backgroundColor':'transparent', 'isStacked':'true'
		  #};
    #return (bar_data, bar_options)

#def line(data_dict, activity_list):
    #line_data = [['Date'] + [str(p.name) for p in activity_list]]
    #for d in data_dict:
	#tmp = [d.isoformat()]
	#for p in activity_list:
	    #if p in data_dict[d]:
		#duration = data_dict[d][p].total_seconds() / 3600
	    #else:
		#duration = 0
	    #tmp.append(duration)
	#if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
	    #line_data.append(tmp)
    #line_options = {'title':'Activities evolution', 'is3D':'true', 'backgroundColor':'transparent'}
    #return (line_data, line_options)

#def line_cumulate(data_dict, activity_list):
    #cum_dict = cumulate(data_dict, activity_list)
    #cum_data = [['Date'] + [str(p.name) for p in activity_list]]
    #for d in cum_dict:
	#tmp = [d.isoformat()]
	#for p in activity_list:
	    #if p in cum_dict[d]:
		#duration = cum_dict[d][p].total_seconds() / 3600
	    #else:
		#duration = 0
	    #tmp.append(duration)
	#if not(sum(tmp[1:]) == 0 and d.weekday() in [5, 6]): #filter non-worked weekend
	    #cum_data.append(tmp)
    #cum_options = { 'title':'Activities evolution (cumulative)', 'is3D':'true'
		#, 'backgroundColor':'transparent'
		#}
    #return (cum_data, cum_options)
	