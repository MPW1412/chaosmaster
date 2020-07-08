from django.contrib import admin
from .models import StoredObjects, Images, Types, NestableObjects


class StoredObjectsAdmin(admin.ModelAdmin):
    list_display = ["uuid","name", "owningEntity", "visibility", "locationEntityUUID","quantity",
        "nestable","type","category","purpose","description","completed","standarisedObject","createdAt",
        "updatedAt"]
    fields = ["uuid","name", "owningEntity", "visibility", "locationEntityUUID","quantity",
    "nestable","type","category","purpose","description","completed","standarisedObject"]
    list_per_page = 10

class ImagesAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "order","path"]
    list_per_page = 10

class TypesAdmin(admin.ModelAdmin):
    list_display = ["id", "type"]
    list_per_page = 10

class NestableObjectsAdmin(admin.ModelAdmin):
    list_display = ["holdingUUID", "containingUUID"]
    list_per_page = 10


admin.site.register(StoredObjects, StoredObjectsAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Types, TypesAdmin)
admin.site.register(NestableObjects, NestableObjectsAdmin)