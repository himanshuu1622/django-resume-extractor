from django.urls import path, re_path
from . import views
from .views import download_file
from django.views.generic.base import TemplateView


urlpatterns = [
    # Public urls
    path('', views.index, name='home'),
    path('upload-resume', views.upload, name='upload_file'),
    path('download/', download_file, name='download_file'),

]