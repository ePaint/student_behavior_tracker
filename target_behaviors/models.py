from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils import Choices
from model_utils.fields import UUIDField, MonitorField
from django.utils.translation import gettext_lazy as _


class Day(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class TargetBehavior(models.Model):
    uuid = UUIDField(version=4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    days = models.ManyToManyField(Day, related_name="target_behaviors")
    periods = models.ManyToManyField(Period, related_name="target_behaviors")
    week_goal_percentage = models.IntegerField(
        default=75, validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('goal')
        verbose_name_plural = _('goals')

    def __str__(self):
        return self.name

    @property
    def max_points(self):
        return self.days.count() * self.periods.count() * 2

    @property
    def week_goal_points(self):
        return int(self.max_points * self.week_goal_percentage / 100 + 0.5)


class TargetBehaviorWeek(models.Model):
    uuid = UUIDField(version=4, editable=False)
    week_number = models.IntegerField()
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="target_behavior_weeks",
    )
    target_behavior = models.ForeignKey(
        TargetBehavior, on_delete=models.CASCADE, related_name="weeks"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.user} - Target {self.target_behavior} - Week {self.week_number}"

    POINTS_MAP = {
        "Achieved Goal": 2,
        "Warning Given": 1,
        "Did Not Achieve Goal": 0,
    }

    @property
    def current_points(self):
        return int(
            sum(self.POINTS_MAP.get(record.value, 0) for record in self.records.all())
        )

    @property
    def current_percentage(self):
        return int(self.current_points / self.target_behavior.max_points * 100 + 0.5)


class TargetBehaviorRecord(models.Model):
    uuid = UUIDField(version=4, editable=False)
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="target_behavior_records",
    )
    target_behavior = models.ForeignKey(
        TargetBehavior, on_delete=models.CASCADE, related_name="records"
    )
    week = models.ForeignKey(
        TargetBehaviorWeek, on_delete=models.CASCADE, related_name="records"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = MonitorField(monitor="value")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="records")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name="records")
    VALUE_CHOICES = Choices("Achieved Goal", "Warning Given", "Did Not Achieve Goal")
    value = models.CharField(
        choices=VALUE_CHOICES, max_length=50, null=True, blank=True
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"User {self.user} - Target {self.target_behavior} - Week {self.week} - Day {self.day} - Period {self.period}"
