# Generated by Django 3.0.7 on 2020-11-07 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploadDB', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbfile',
            name='remark',
        ),
    ]
