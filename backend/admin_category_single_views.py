from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import QueryDict

from .models import Categories, Requests

from .category_serializer import CategorySerializer

class AdminCategorySingleView(APIView):
    def get(self, request, pk):
        try:
            category = get_object_or_404(Categories.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        serializer = CategorySerializer(category, many=False)

        return Response({"result": serializer.data, "error": None})

    def put(self, request, pk):
        try:
            category = get_object_or_404(Categories.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        post_params = QueryDict(request.body)
        try:
            name = post_params['name']
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})

        if name is not None:
            category.name = name
            try:
                category.save()
            except Exception:
                return Response({"result": None, "error": "The request could not be processed due to a syntax error."})

        return AdminCategorySingleView.get(self, request, category.pk)

    def delete(self, request, pk):
        try:
            category = get_object_or_404(Categories.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        try:
            category.delete()
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})

        requests = Requests.objects.all()
        for item in requests:
            list_categories = item.categories.all()
            if not list_categories:
                item.is_marked_up = False
                try:
                    item.save()
                except Exception:
                    return Response(
                        {"result": None, "error": "The request could not be processed due to a syntax error."})

        return Response({"result": None, "error": None})