# Generated by Django 4.2.5 on 2023-10-01 11:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hn_follow_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="hnuser",
            name="submissions",
            field=models.JSONField(null=True),
        ),
    ]
