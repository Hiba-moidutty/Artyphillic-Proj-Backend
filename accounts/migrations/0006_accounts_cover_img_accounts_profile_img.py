# Generated by Django 4.1.3 on 2023-07-08 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_address_artist_alter_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='cover_img',
            field=models.ImageField(null=True, upload_to='profiles'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='profiles'),
        ),
    ]
