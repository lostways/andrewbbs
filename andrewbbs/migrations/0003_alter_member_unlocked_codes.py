# Generated by Django 4.1.7 on 2023-03-20 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("andrewbbs", "0002_alter_member_unlocked_codes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="unlocked_codes",
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
