# Generated by Django 2.2.7 on 2019-11-15 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set(),
        ),
    ]
