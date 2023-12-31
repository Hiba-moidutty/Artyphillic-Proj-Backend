# Generated by Django 4.2 on 2023-05-20 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_blocked_accounts_is_blocked'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_address', models.CharField(max_length=150)),
                ('alt_ph_number', models.CharField(max_length=13)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('landmark', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
