# Generated by Django 4.1.1 on 2022-12-12 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0003_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='username_foreign',
        ),
    ]