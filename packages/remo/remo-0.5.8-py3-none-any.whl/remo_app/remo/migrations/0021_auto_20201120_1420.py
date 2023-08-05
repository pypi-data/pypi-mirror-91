# Generated by Django 2.2.11 on 2020-11-20 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remo', '0020_uploadsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadsession',
            name='dataset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='remo.Dataset'),
        ),
        migrations.AlterField(
            model_name='uploadsession',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
