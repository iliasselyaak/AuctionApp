# Generated by Django 4.1.1 on 2022-12-16 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0011_remove_user_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='username_foreign',
        ),
    ]