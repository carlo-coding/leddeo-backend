# Generated by Django 4.1.5 on 2023-02-23 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_remove_plan_id_plan_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='lookup_key',
            field=models.CharField(default='59', max_length=100),
            preserve_default=False,
        ),
    ]
