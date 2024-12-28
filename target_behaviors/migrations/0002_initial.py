# Generated by Django 5.1.4 on 2024-12-28 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("target_behaviors", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="targetbehaviorrecord",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="target_behavior_records",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="targetbehaviorweek",
            name="target_behavior",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="weeks",
                to="target_behaviors.targetbehavior",
            ),
        ),
        migrations.AddField(
            model_name="targetbehaviorweek",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="target_behavior_weeks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="targetbehaviorrecord",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="records",
                to="target_behaviors.targetbehaviorweek",
            ),
        ),
    ]
