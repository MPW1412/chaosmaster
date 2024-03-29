# Generated by Django 3.0.7 on 2020-06-14 06:06

from django.db import migrations, models
import django.db.models.deletion
import inventory.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoredObjects',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('owningEntity', models.UUIDField(blank=True, null=True, validators=[inventory.models.validate_uuid])),
                ('visibility', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('locationEntityUUID', models.UUIDField(blank=True, null=True, validators=[inventory.models.validate_uuid])),
                ('quantity', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('nestable', models.BooleanField(default=False)),
                ('type', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('category', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('purpose', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('standarisedObject', models.UUIDField(blank=True, null=True, validators=[inventory.models.validate_uuid])),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Stored Objects',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.DecimalField(decimal_places=0, default=0, max_digits=10)),
                ('path', models.ImageField(upload_to='images/')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('uuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.StoredObjects')),
            ],
            options={
                'verbose_name_plural': 'Images',
                'unique_together': {('order', 'uuid')},
            },
        ),
    ]
