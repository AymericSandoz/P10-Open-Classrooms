# Generated by Django 3.2.12 on 2024-02-11 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_project_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='project.user'),
            preserve_default=False,
        ),
    ]
