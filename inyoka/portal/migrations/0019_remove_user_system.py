# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_suggest_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='system',
        ),
    ]
