from django.contrib import admin
from models import ( DailyCostPerTask, DailyCostPerTaskPerUser,
                    DailyDurationPerTask, DailyDurationPerTaskPerUser )

admin.site.register(DailyDurationPerTaskPerUser)
admin.site.register(DailyDurationPerTask)
admin.site.register(DailyCostPerTaskPerUser)
admin.site.register(DailyCostPerTask)
