# Generated by Django 4.0.3 on 2022-04-04 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20200902_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
