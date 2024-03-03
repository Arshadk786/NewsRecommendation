from django.urls import path
from fake_news import views

urlpatterns = [
    path("",views.index),
    path('detect_fake_news/', views.detect_fake_news, name='detect-fake-news'),
    
]

# 