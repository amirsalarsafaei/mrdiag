# Generated by Django 4.2.9 on 2024-02-03 19:59

import diag_report.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diag_report', '0002_diagreport_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=diag_report.models.upload_to),
        ),
    ]