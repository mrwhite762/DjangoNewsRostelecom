# Generated by Django 4.2.6 on 2023-12-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_account_address_account_instagram_account_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N/A', 'Not answered')], max_length=20, null=True),
        ),
    ]