# Generated by Django 3.2.12 on 2024-02-18 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_remove_comment_link_to_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
            preserve_default=False,
        ),
    ]