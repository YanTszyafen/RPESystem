# Generated by Django 2.2 on 2022-01-15 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20220115_0252'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='telephone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
