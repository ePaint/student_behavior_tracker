from django.db import models


class Day(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class TargetBehavior(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    days = models.ManyToManyField(Day, related_name='target_behaviors')
    periods = models.ManyToManyField(Period, related_name='target_behaviors')

    def __str__(self):
        return self.name


class TargetBehaviorWeek(models.Model):
    week_number = models.IntegerField()
    target_behavior = models.ForeignKey(TargetBehavior, on_delete=models.CASCADE, related_name='weeks')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class RecordValue(models.IntegerChoices):
    DID_NOT_ACHIEVE_GOAL = 0
    WARNING_GIVEN = 1
    ACHIEVED_GOAL = 2

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class TargetBehaviorRecord(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='target_behavior_records')
    target_behavior = models.ForeignKey(TargetBehavior, on_delete=models.CASCADE, related_name='records')
    week = models.ForeignKey(TargetBehaviorWeek, on_delete=models.CASCADE, related_name='records')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='records')
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='records')
    value = models.IntegerField(choices=RecordValue.choices)
    notes = models.TextField()
