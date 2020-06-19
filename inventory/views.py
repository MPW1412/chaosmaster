import json
from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from uuid import UUID
from django.core.exceptions import ValidationError

from .models import StoredObjects, Images
from .serializers import StoredObjectsSerializer, ImagesSerializer, \
    CreateStoredObjectsSerializer, CreateImagesSerializer


class StoredObjectsList(APIView):

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

    def post(self, request, format=None):
        print(request.data)
        serializer = CreateStoredObjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    "status": True,
                    "code" : status.HTTP_201_CREATED,
                    "message" : "Stored Object Created Successfully!",
                    "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Error in Stored Object Creation!",
                    "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class StoredObjectsDetail(APIView):

    def validate_url(self, pk):
        try:
            uuid_string = UUID(pk).version
            return True
        except:
            return False

    def get_object(self, pk):
        try:
            return StoredObjects.objects.get(pk=pk)
        except StoredObjects.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        if not self.validate_url(pk):
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)
     
        stored_object = self.get_object(pk)
        if not stored_object:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Store Object Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = StoredObjectsSerializer(stored_object, 
                                    context={"request" : request})  
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Successfully fetched Stored Object!",
                    "data": serializer.data
            }, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        if not self.validate_url(pk):
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)

        stored_object = self.get_object(pk)
        if not stored_object:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Store Object Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = CreateStoredObjectsSerializer(stored_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Stored Object Updated Successfully!",
                    "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Error in Stored Object updation!",
                    "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        if not self.validate_url(pk):
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)

        stored_object = self.get_object(pk)
        if not stored_object:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Store Object Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)
        stored_object.delete()
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Stored Object Deleted Successfully!"
            }, status=status.HTTP_200_OK)

class ImagesList(APIView):
    def validate_url(self, pk):
        try:
            uuid_string = UUID(pk).version
            return True
        except:
            return False

    def get(self, request, pk):
        if not self.validate_url(pk):
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)
        images = Images.objects.filter(uuid = pk)
        serializer = ImagesSerializer(images, 
                                    many=True, context={"request" : request})
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Successfully fetched all Images of stored Object!",
                    "total_count" : images.count(),
                    "data": serializer.data
            }, status=status.HTTP_200_OK)    

    def post(self, request, pk, format=None):
        if not self.validate_url(pk):
            return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Invalid Url"
            }, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        request.data['uuid'] = pk
        print(request.data)
        serializer = CreateImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                    "status": True,
                    "code" : status.HTTP_201_CREATED,
                    "message" : "Image Created Successfully!",
                    "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Error in Image Creation!",
                    "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ImagesDetail(APIView):

    def get_object(self, pk):
        try:
            return Images.objects.get(pk=pk)
        except Images.DoesNotExist:
            return False

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        if not image:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Image Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ImagesSerializer(image, context={"request" : request})  
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Successfully fetched Image!",
                    "data": serializer.data
            }, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        print(image.path)
        if not image:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Image Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)
        request.data['path'] = image.path
        request.data['uuid'] = str(image.uuid)  
        print(request.data)  
        serializer = CreateImagesSerializer(image, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Image Updated Successfully!",
                    "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                    "status": False,
                    "code" : status.HTTP_400_BAD_REQUEST,
                    "message" : "Error in Image updation!",
                    "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        if not image:
            return Response({
                    "status": False,
                    "code" : status.HTTP_404_NOT_FOUND,
                    "message" : "Image Not Exists"
            }, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response({
                    "status": True,
                    "code" : status.HTTP_200_OK,
                    "message" : "Image Deleted Successfully!"
            }, status=status.HTTP_200_OK)

  