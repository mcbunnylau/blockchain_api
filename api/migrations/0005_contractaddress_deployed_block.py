# Generated by Django 3.2.7 on 2021-10-06 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_logevent_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractaddress',
            name='deployed_block',
            field=models.IntegerField(default=11348423),
            preserve_default=False,
        ),
    ]
