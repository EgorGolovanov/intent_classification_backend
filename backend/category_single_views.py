from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categories

from .category_serializer import CategorySerializer

class CategorySingleView(APIView):
    def get(self, request, pk):
        try:
            categories = get_object_or_404(Categories.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        serializer = CategorySerializer(categories, many=False)
        return Response({"result": serializer.data, "error": None})