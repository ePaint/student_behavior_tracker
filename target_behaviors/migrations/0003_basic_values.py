from django.db import migrations


class Migration(migrations.Migration):
    def custom_task(apps, schema_editor):
        to_create = {
            "Day": [
                {"name": "Monday"},
                {"name": "Tuesday"},
                {"name": "Wednesday"},
                {"name": "Thursday"},
                {"name": "Friday"},
                {"name": "Saturday"},
                {"name": "Sunday"},
            ],
            "Period": [
                {"name": "P1"},
                {"name": "P2"},
                {"name": "P3"},
                {"name": "P4"},
                {"name": "P5"},
                {"name": "P6"},
                {"name": "P7"},
                {"name": "P8"},
                {"name": "Lunch"},
            ],
        }
        for model_name, entries in to_create.items():
            model = apps.get_model("target_behaviors", model_name)
            for entry in entries:
                model.objects.get_or_create(**entry)

    dependencies = [
        ("target_behaviors", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(custom_task, migrations.RunPython.noop),
    ]
