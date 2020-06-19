from django.urls import include,path
from rest_framework import routers
from inventory.views import StoredObjectsList, ImagesList, \
    StoredObjectsDetail, ImagesDetail

urlpatterns = [
    path('stored-objects/', StoredObjectsList.as_view(), name="stored_objects_api"),
    path('stored-objects/<str:pk>/', StoredObjectsDetail.as_view(), name="stored_object_detail_api"),
    path('images/<str:pk>/', ImagesList.as_view(), name="images_api"),
    path('images/change/<int:pk>/', ImagesDetail.as_view(), name="images_detail_api"),
]
