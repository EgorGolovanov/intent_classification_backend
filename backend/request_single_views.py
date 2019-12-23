# noinspection PyUnresolvedReferences
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import QueryDict

from .models import Requests, Categories
# noinspection PyUnresolvedReferences
from .request_serializer import RequestSerializer

class RequestSingleView(APIView):
    def get(self, request, pk):
        try:
            request_object = get_object_or_404(Requests.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        serializer = RequestSerializer(request_object, many=False)

        return Response({"result": serializer.data, "error": None})

    def put(self, request, pk):
        try:
            request_object = get_object_or_404(Requests.objects.all(), pk=pk)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        post_params = QueryDict(request.body)
        category_ids = post_params.getlist('category_ids')

        if category_ids:
            request_object.is_marked_up = True
            try:
                request_object.save()
            except Exception:
                return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
            for category_id in category_ids:
                category = Categories.objects.get(id=category_id)
                if category is not None:
                    category.requests_set.add(request_object)

        return RequestSingleView.get(self, request, request_object.pk)

