# Generated by Django 4.2 on 2023-05-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
