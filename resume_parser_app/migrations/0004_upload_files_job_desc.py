# Generated by Django 4.2 on 2023-05-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_parser_app', '0003_alter_upload_files_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload_files',
            name='job_desc',
            field=models.TextField(default='jd not entered', max_length=300),
        ),
    ]
