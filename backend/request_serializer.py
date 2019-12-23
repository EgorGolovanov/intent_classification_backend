from rest_framework import serializers
from .models import Requests
from .category_serializer import CategorySerializer

class RequestSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Requests
        fields = '__all__'
