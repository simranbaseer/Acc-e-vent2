# Generated by Django 2.2.4 on 2019-08-06 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagboard', '0004_parttags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='id',
        ),
        migrations.AlterField(
            model_name='users',
            name='uid',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]