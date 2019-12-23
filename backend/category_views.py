# noinspection PyUnresolvedReferences
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Categories
# noinspection PyUnresolvedReferences
from .category_serializer import CategorySerializer

class CategoryView(APIView):
    def get(self, request):
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"result": serializer.data, "error": None})
