# Generated by Django 4.1.1 on 2022-12-11 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0002_alter_item_bid_alter_user_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='1970-01-01'),
        ),
    ]