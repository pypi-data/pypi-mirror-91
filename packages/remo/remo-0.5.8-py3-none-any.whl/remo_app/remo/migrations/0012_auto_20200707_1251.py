# Generated by Django 2.2.11 on 2020-07-07 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remo', '0011_agrinstallations_agrstats_agrusage_localstats_localusage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agrstats',
            old_name='created_at',
            new_name='snapshot_time',
        ),
    ]
