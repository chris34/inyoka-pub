# Generated by Django 1.11.25 on 2019-10-27 18:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikhaya', '0008_comment_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime.utcnow, verbose_name='Datum'),
        ),
    ]
