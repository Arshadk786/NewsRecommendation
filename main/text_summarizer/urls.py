from django.urls import path
from text_summarizer import views

urlpatterns = [
    path("",views.index),
    path("summarize/",views.summarize),

]