# Generated by Django 4.2.1 on 2023-05-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthplatform', '0003_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=2, null=True),
        ),
    ]
