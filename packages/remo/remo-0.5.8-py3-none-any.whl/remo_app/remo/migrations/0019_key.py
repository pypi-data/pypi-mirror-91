# Generated by Django 2.2.11 on 2020-09-28 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remo', '0018_auto_20200923_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(blank=True, default='', null=True)),
            ],
            options={
                'db_table': 'keys',
            },
        ),
    ]
