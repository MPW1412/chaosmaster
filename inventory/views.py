import json
from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from uuid import UUID
from django.core.exceptions import ValidationError

from .models import StoredObjects, Images
from .serializers import StoredObjectsSerializer, ImagesSerializer


class getStoredObjectsList(APIView):

    def get(self, request):
        stored_objects = StoredObjects.objects.all()
        serializer = StoredObjectsSerializer(stored_objects, 
                                    many=True, context={"request" : request})
        # return Response(serializer.data, status=status.HTTP_200_OK)   
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Successfully fetched all Stored Objects!",
                    "total_count" : stored_objects.count(),
                    "data": serializer.data
            }, status=status.HTTP_200_OK)

class getImagesList(APIView):

    def get(self, request, fk):
        try:
            uuid_string = UUID(fk, version=4)
        except:
            # raise ValidationError("Not a Valid UUID hexstring")
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)   
        images = Images.objects.filter(uuid = fk)
        serializer = ImagesSerializer(images, 
                                    many=True, context={"request" : request})
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Successfully fetched all Images of stored Object!",
                    "total_count" : images.count(),
                    "data": serializer.data
            }, status=status.HTTP_200_OK)    

  