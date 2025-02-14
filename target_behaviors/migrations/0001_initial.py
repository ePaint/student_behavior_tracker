# Generated by Django 5.1.4 on 2024-12-28 14:34

import django.db.models.deletion
import model_utils.fields
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Period",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TargetBehaviorWeek",
            fields=[
                (
                    "uuid",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("week_number", models.IntegerField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TargetBehavior",
            fields=[
                (
                    "uuid",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                (
                    "days",
                    models.ManyToManyField(
                        related_name="target_behaviors", to="target_behaviors.day"
                    ),
                ),
                (
                    "periods",
                    models.ManyToManyField(
                        related_name="target_behaviors", to="target_behaviors.period"
                    ),
                ),
                (
                    "week_goal_percentage",
                    models.IntegerField(
                        default=75,
                        validators=[MaxValueValidator(100), MinValueValidator(0)],
                    ),
                ),
                ("deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="TargetBehaviorRecord",
            fields=[
                (
                    "uuid",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "date_modified",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now, monitor="value"
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Achieved Goal", "Achieved Goal"),
                            ("Warning Given", "Warning Given"),
                            ("Did Not Achieve Goal", "Did Not Achieve Goal"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="target_behaviors.day",
                    ),
                ),
                (
                    "period",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="target_behaviors.period",
                    ),
                ),
                (
                    "target_behavior",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="target_behaviors.targetbehavior",
                    ),
                ),
            ],
        ),
    ]
