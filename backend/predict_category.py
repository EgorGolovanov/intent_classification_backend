# noinspection PyUnresolvedReferences
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import QueryDict
from intents_classifier import module
from .category_single_views import CategorySingleView
from .models import Requests, Categories

import pandas as pd

class PredictCategory(APIView):
    def get(self, request):
        body_params = QueryDict(request.body)
        try:
            content = body_params['content']
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        id_predict_category = module.predict(content)
        if id_predict_category == -1:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        return CategorySingleView.get(self, request, id_predict_category)


    def put(self, request):
        list_requests = []
        list_categories = []
        requests = Requests.objects.all()
        for request in requests:
            list_categories_for_one_request = request.categories.all()
            if request.is_marked_up:
                list_categories.append(list_categories_for_one_request[0].id)
                list_requests.append(request.content)
        try:
            history = module.fit(list_requests, list_categories)
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        return Response({"result": "Модель переобучена"})

    def post(self, request):
        path = self.request.query_params.get('path', None)
        #'C:/Users/egorg/Downloads/Telegram Desktop/russian_train.xlsx'
        try:
            file_excel = pd.read_excel(path, sheet_name='russian_train')
        except Exception:
            return Response({"result": None, "error": "The request could not be processed due to a syntax error."})
        file_excel[:6]
        unique_intents = file_excel.columns
        for intent in unique_intents:
            for text in file_excel[intent]:
                if pd.isnull(text):
                    break
                else:
                    content = text
                    category_id = intent
                    new_request = Requests.objects.create(content=content)
                    new_request.is_marked_up = True
                    new_request.save()
                    category = Categories.objects.get(id=category_id)
                    if category:
                        category.requests_set.add(new_request)
        return Response({"result": "success"})