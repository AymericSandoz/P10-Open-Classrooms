# Generated by Django 3.2.12 on 2024-02-18 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_contributor_project'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user', 'project')},
        ),
    ]