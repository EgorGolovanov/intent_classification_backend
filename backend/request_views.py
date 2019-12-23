# noinspection PyUnresolvedReferences
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from .models import Requests, Categories
# noinspection PyUnresolvedReferences
from .request_serializer import RequestSerializer

class RequestView(APIView):

    def get(self, request):
        queryset = Requests.objects.all().order_by('id')

        marked_up = bool(self.request.query_params.get('is_marked_up', None))
        q = self.request.query_params.get('q', None)
        page = int(self.request.query_params.get('page', 1))
        per = int(self.request.query_params.get('per', 25))

        if marked_up is not None:
            queryset = queryset.filter(is_marked_up=marked_up)

        if q is not None:
            queryset = queryset.filter(content__contains=q)

        paginator = Paginator(queryset, per)  # Show 25 contacts per page
        result = paginator.get_page(page)
        next_page = None

        if page + 1 <= paginator.num_pages:
            next_page = page + 1

        serializer = RequestSerializer(result, many=True)

        return Response({"result": serializer.data,
                         "pagination":
                             {
                                 "total_pages": paginator.num_pages,
                                 "total_count": paginator.count,
                                 "next_page": next_page
                             },
                         "error": None})
