# Generated by Django 4.1 on 2023-12-07 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opiniones', '0002_alter_opinion_nota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='opinion_id',
        ),
    ]