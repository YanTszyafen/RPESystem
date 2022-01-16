from django.urls import path
from home.views import IndexView, DetailView, PredictView
urlpatterns = [
    path('',IndexView.as_view(),name='index'),

    path('detail/',DetailView.as_view(),name='detail'),

    path('predict/', PredictView.as_view(), name='predict')
]