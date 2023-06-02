from django.urls import path
from . import views

app_name = "resume_parser_app"

urlpatterns = [
    path("", views.index),
    path("upload", views.send_files, name="uploads"),
    path("results", views.resume_parser_model, name="result"),
    path("export_json", views.export_json, name="json"),
    path("export_csv", views.export_csv, name="csv"),
    path("export_xlsx", views.export_xlsx, name="xlsx")

]