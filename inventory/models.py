import re
import os
import uuid
from uuid import UUID
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from django.db import models

def validate_uuid(value):
    try:
        uuid_string = UUID(value, version=4)
    except:
        raise ValidationError("Not a Valid UUID") 

def restrict_total_image(value):
    images = Images.objects.filter(uuid=value)
    if images.count() > 10:
        raise ValidationError('Stored object already have a 10 images')

def is_nestable(value):
    objectData = StoredObjects.objects.filter(uuid=str(value)).first()
    if not objectData.nestable:
        raise ValidationError('Stored object is not nestable')
    return True

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance, ext)
        return os.path.join(self.sub_path, filename)

class Types(models.Model):
    type = models.CharField(max_length = 50, unique = True,
                        verbose_name = "Type")

    class Meta:
        verbose_name_plural = "Types"
    
    def __str__(self):
        return self.type

class StoredObjects(models.Model):
    uuid = models.UUIDField(primary_key = True,
                                default = uuid.uuid4)
    name = models.CharField(max_length = 20, null = True, blank = True,
                                verbose_name = "Name")
    owningEntity = models.CharField(max_length = 36, null = True, blank = True, 
                                verbose_name = "Owning Entity",
                                validators = [validate_uuid])
    visibility = models.IntegerField(null = True, blank = True,
                                verbose_name = "Visibility")
    locationEntityUUID = models.CharField(max_length = 36, null = True, blank = True, 
                                verbose_name = "Location Entity UUID", 
                                validators = [validate_uuid])
    quantity = models.IntegerField(null = True, blank = True,
                                verbose_name = "Quantity")
    nestable = models.BooleanField(default=False,
                                verbose_name = "Nestable")
    type = models.ForeignKey(Types, null = True, blank = True,
                                related_name = 'types',
                                on_delete = models.SET_NULL,
                                verbose_name = "Type")
    category = models.IntegerField(null = True, blank = True,
                                verbose_name = "Category")
    purpose = models.CharField(max_length = 50, null = True, blank = True,
                                verbose_name = "Purpose")
    description = models.TextField(max_length = 200, null = True, blank = True,
                                verbose_name = "Description")
    completed = models.BooleanField(default = False,
                                verbose_name = "Completed")
    standarisedObject = models.CharField(max_length = 36,null = True, blank = True, 
                                verbose_name = "Standarised Object",
                                validators = [validate_uuid])
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Stored Objects"

    def __str__(self):
        return str(self.uuid)

class Images(models.Model):
    uuid = models.ForeignKey(StoredObjects,
                    validators = [restrict_total_image],
                    related_name = 'images',
                    on_delete = models.CASCADE)
    order = models.IntegerField()
    path = models.ImageField(upload_to = UploadToPathAndRename('images/'),
                    height_field=None, width_field=None)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Images"
        unique_together = ['order', 'uuid']
    
    def __str__(self):
        return '{}-{}'.format(str(self.uuid.uuid), self.order)


class NestableObjects(models.Model):
    holdingUUID = models.ForeignKey(StoredObjects,
                    related_name = 'holdingObject',
                    on_delete = models.CASCADE)
    containingUUID = models.ForeignKey(StoredObjects,
                    validators = [is_nestable],
                    unique= True,
                    related_name = 'containingObject',
                    on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = "Nestable Objects"
        unique_together = ['holdingUUID', 'containingUUID']

    def __str__(self):
        return '{}-{}'.format(str(self.holdingUUID.uuid), self.containingUUID.uuid)


