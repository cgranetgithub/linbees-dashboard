import datetime
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

#def records2days(queryset):
    #one_day = datetime.timedelta(1)
    #date_dict = defaultdict(defaultdict)
    #for record in queryset:
	##activity_set.add(record.activity)
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
		#date_dict[start_date][record.activity] += duration
	    ##several days
	    #else:
		#iter_date = start_date
		##first day
		#duration = datetime.datetime(iter_date.year, iter_date.month
					    #, iter_date.day
					    #, tzinfo=record.start().tzinfo) + one_day - record.start()
		#date_dict[iter_date][record.activity] += duration
		##days in the middle
		#while iter_date != end_date:
		    #duration = datetime.timedelta(1)
		    #if iter_date not in date_dict:
			#date_dict[iter_date] = defaultdict(datetime.timedelta)
		    #date_dict[iter_date][record.activity] += duration
		    #iter_date += one_day
		##last day
		#duration = record.end() - datetime.datetime(iter_date.year, iter_date.month
						      #, iter_date.day
						      #, tzinfo=record.end().tzinfo)
		#date_dict[iter_date][record.activity] += duration
    #data_dict = OrderedDict(sorted(date_dict.items(), key=lambda t: t[0]))
    #return data_dict

#def activitiesAlongTime2(workspace, activity_id=None):
    #t = datetime.datetime.now()
    #if activity_id is not None:
        #qs = Record.for_tenant(workspace).objects.filter(activity__id=activity_id)
        #activities = [Activity.for_tenant(workspace).objects.get(pk=activity_id)]
    #else:
        #qs = Record.for_tenant(workspace).objects.all()
        #p_dicts = Record.for_tenant(workspace).objects.values("activity")
        #p_list = [p["activity"] for p in p_dicts]
        #activities = [Activity.for_tenant(workspace).objects.get(pk=p) for p in set(p_list)]
    #if qs.count() == 0:
        #return ({}, [])
    #data_dict = records2days(qs)
    #return (data_dict, activities)

#def cumulate(data_dict, activity_list):
    #if data_dict == {}:
          #return {}
    #cum_dict = defaultdict(defaultdict)
    #dates = data_dict.keys()
    #prev_date = dates[0]
    #cum_dict[prev_date] = data_dict[prev_date]
    #for date in dates[1:]:
        #cum_dict[date] = defaultdict(datetime.timedelta)
        #for p in activity_list:
            #cum_dict[date][p] = cum_dict[prev_date][p] + data_dict[date][p]
        #prev_date = date
    #ret_dict = OrderedDict(sorted(cum_dict.items(), key=lambda t: t[0]))
    #return ret_dict

#def activitiesSum(workspace):
    #activities = Activity.for_tenant(workspace).objects.all()
    #time_dict = defaultdict(datetime.timedelta)
    #for p in activities:
        #records = Record.for_tenant(workspace).objects.filter(activity__name__exact=p.name)
        #sum_time = datetime.timedelta(0)
        #for r in records:
                #if r.end() is not None:
                        #sum_time += r.end() - r.start()
        #time_dict[p] = sum_time
    #return time_dict
