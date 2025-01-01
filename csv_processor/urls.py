from django.urls import path
from .views import CSVUploadAPIView,home

urlpatterns = [
    path('upload-csv', CSVUploadAPIView.as_view(), name='upload_csv'),
    path('home', home, name='home'),
]