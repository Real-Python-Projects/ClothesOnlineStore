# Generated by Django 3.1.7 on 2021-04-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(default=254, max_length=15),
            preserve_default=False,
        ),
    ]
