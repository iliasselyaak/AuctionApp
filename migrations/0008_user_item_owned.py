# Generated by Django 4.1.2 on 2022-12-15 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctionapp', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Item_owned',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctionapp.item'),
        ),
    ]
