# Generated by Django 2.2.7 on 2019-12-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('', 'default')], max_length=100),
        ),
    ]
