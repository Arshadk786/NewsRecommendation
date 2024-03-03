from django.urls import path
from news_recommendation import views


urlpatterns = [
    path("",views.index),
    path("recommend/",views.recommend),

]