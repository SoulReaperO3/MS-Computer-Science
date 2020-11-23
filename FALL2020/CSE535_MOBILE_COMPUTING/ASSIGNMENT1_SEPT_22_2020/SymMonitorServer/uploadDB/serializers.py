from rest_framework import serializers
from .models import dbFile 

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = dbFile
    fields = ('file', 'timestamp')
