# Generated by Django 3.1 on 2020-09-01 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olms', '0011_auto_20200901_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('granted', 'granted'), ('rejected', 'rejected')], default='submitted', max_length=9),
        ),
    ]
