# Generated by Django 3.1 on 2020-08-31 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olms', '0007_auto_20200831_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leaveuser', to='olms.userprofile'),
        ),
    ]