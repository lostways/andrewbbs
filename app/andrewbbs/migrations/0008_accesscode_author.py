# Generated by Django 4.1.10 on 2023-10-07 03:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("andrewbbs", "0007_alter_message_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="accesscode",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="access_codes",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
