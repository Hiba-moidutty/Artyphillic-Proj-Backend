# Generated by Django 4.1.3 on 2023-06-20 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0011_artist_from_google'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='username',
            new_name='artistname',
        ),
        migrations.RenameField(
            model_name='artist',
            old_name='artist_name',
            new_name='full_name',
        ),
    ]