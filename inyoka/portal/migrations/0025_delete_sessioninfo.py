# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0024_auto_20170429_1526'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SessionInfo',
        ),
    ]
