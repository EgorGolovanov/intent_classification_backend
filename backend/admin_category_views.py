# noinspection PyUnresolvedReferences
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import QueryDict

from .models import Categories
# noinspection PyUnresolvedReferences
from .category_serializer import CategorySerializer
from .admin_category_single_views import AdminCategorySingleView

class AdminCategoryView(APIView):
    def get(self, request):
        categories = Categories.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response({"result": serializer.data, "error": None})

    def post(self, request):
        post_params = QueryDict(request.body)
        name = post_params['name']
        new_category = Categories.objects.create(name=name)

        return AdminCategorySingleView.get(self, request, new_category.pk)

