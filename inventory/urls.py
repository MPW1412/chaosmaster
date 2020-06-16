from django.urls import include,path
from rest_framework import routers
from . import views

urlpatterns = [
    path('stored-objects/', views.getStoredObjectsList.as_view(), name="get_stored_objects_api"),
    path('images/<str:fk>/', views.getImagesList.as_view(), name="get_images_api"),
]
