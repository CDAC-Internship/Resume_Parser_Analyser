import os
from django.db import models

# Create your models here.

class upload_files (models.Model) :

    file_name = models.CharField(max_length=250)
    files = models.FileField(upload_to="")

    job_desc = models.TextField(max_length=300, default="jd not entered")