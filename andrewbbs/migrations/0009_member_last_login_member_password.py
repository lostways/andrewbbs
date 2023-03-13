# Generated by Django 4.1.7 on 2023-03-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("andrewbbs", "0008_alter_member_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="member",
            name="password",
            field=models.CharField(
                default="notatpassword123", max_length=128, verbose_name="password"
            ),
            preserve_default=False,
        ),
    ]
