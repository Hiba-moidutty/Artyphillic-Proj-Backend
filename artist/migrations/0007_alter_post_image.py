# Generated by Django 4.1.3 on 2023-06-06 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='posts'),
        ),
    ]