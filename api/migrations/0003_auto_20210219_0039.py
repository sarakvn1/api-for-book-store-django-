# Generated by Django 3.1.4 on 2021-02-19 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210218_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.address'),
        ),
    ]
