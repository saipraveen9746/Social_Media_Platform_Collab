# Generated by Django 5.0.4 on 2024-05-13 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0002_customuser_follower_customuser_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='location',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
