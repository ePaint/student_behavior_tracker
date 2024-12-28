from django.contrib import admin
from target_behaviors.models import Day, Period, TargetBehavior, TargetBehaviorWeek, TargetBehaviorRecord

admin.site.register(Day)
admin.site.register(Period)
admin.site.register(TargetBehavior)
admin.site.register(TargetBehaviorWeek)
admin.site.register(TargetBehaviorRecord)

