# Generated by Django 3.1.4 on 2021-02-22 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20210222_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='EnSummary',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='FaSummary',
            field=models.CharField(blank=True, max_length=350, null=True),
        ),
    ]
