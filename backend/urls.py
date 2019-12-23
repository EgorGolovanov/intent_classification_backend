from django.urls import path
from .request_views import RequestView
from .request_single_views import RequestSingleView
from .category_views import CategoryView
from .category_single_views import CategorySingleView
from .admin_request_single_views import AdminRequestSingleView
from .admin_request_views import AdminRequestView
from .admin_category_views import AdminCategoryView
from .admin_category_single_views import AdminCategorySingleView
from .predict_category import PredictCategory

app_name = "requests"

urlpatterns = [
    path('requests/', RequestView.as_view()),
    path('requests/<int:pk>', RequestSingleView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('categories/<int:pk>', CategorySingleView.as_view()),
    path('admin/requests/', AdminRequestView.as_view()),
    path('admin/requests/<int:pk>', AdminRequestSingleView.as_view()),
    path('admin/categories/', AdminCategoryView.as_view()),
    path('admin/categories/<int:pk>', AdminCategorySingleView.as_view()),
    path('predict_category/', PredictCategory.as_view())
]