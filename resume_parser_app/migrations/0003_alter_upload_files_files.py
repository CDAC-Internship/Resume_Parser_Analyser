# Generated by Django 4.2 on 2023-05-01 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_parser_app', '0002_alter_upload_files_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload_files',
            name='files',
            field=models.FileField(upload_to=''),
        ),
    ]