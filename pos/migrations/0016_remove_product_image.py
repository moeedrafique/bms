# Generated by Django 4.2.7 on 2023-12-03 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0015_branch_branch_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
