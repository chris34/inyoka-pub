# Generated by Django 2.2.28 on 2023-03-12 17:04

from django.db import migrations
import inyoka.utils.database


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_auto_20191027_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='value',
            field=inyoka.utils.database.InyokaMarkupField(application='wiki', force_existing=False, simplify=False),
        ),
    ]
