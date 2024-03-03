import json
from django.http import HttpResponse
import pandas as pd
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
# from rest_framework.permissions import IsAuthenticated

def load_news_data():
    try:
        response = requests.get('https://newsapi.org/v2/everything?sources=the-times-of-india&apiKey=f920a5d9981e42de91c052c8471db7a2')
        if response.status_code == 200:
            news_data = response.json()['articles']
            df = pd.DataFrame(news_data)[['title', 'description', 'url', 'publishedAt','urlToImage']]
            df['tags'] = df['title'] + df['description']
            df['tags'] = df['tags'].apply(lambda x: x.lower())
            return df
        else:
            raise Exception(response.text)
    except Exception as e:
        raise e
    
def recommend_articles(user_activities, num_recommendations=10):
    try:
        df = load_news_data()

        # Initialize TF-IDF vectorizer
        tfidf_vectorizer = TfidfVectorizer(max_features=1689, stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(df['tags'])
        # Combine the user's activities into a single string
        user_activity_text = ' '.join(user_activities)

        # Transform the user's activity using the same TF-IDF vectorizer
        user_profile = tfidf_vectorizer.transform([user_activity_text])

        # Calculate similarity between user profile and all articles
        cosine_scores = cosine_similarity(user_profile, tfidf_matrix)

        # Get indices of articles sorted by similarity score
        article_indices = cosine_scores.argsort()[0][::-1]

        # Recommend top num_recommendations articles
        recommended_articles = df.iloc[article_indices[:num_recommendations]]

        # Create a DataFrame with titles and links
        recommended_df = recommended_articles[['title', 'url', 'description', 'publishedAt','urlToImage']]
        return recommended_df.to_dict(orient='records')
    except Exception as e:
        raise e

# Create your views here.

def index(request):
    return HttpResponse("Welcome to index")

@api_view(['POST'])
def facultyLogin(request):
    serializer=AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    print("Request Data:", request.data)
    user=serializer.validated_data['user']
    print("User:", user)
    print("Hello world")
    if  not user.is_staff:
        return Response({"detail": "Login not allowed. Contact the superuser to enable login."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        _,token=AuthToken.objects.create(user)
        
        return Response({'user_info': user.pk,"token":token})

# @require_POST
@csrf_exempt
def recommend(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        data = json.loads(request.body)
        print(type(data))
        # print(data)
        user_activities = data
        # user_activities = request.POST.getlist("user_activities")
        # user_activities = request.getlist('user_activities[]',[])
        # print(type(user_activities))
        # print("--> this was my list",user_activities)
        if not user_activities:
            return HttpResponseBadRequest("User activities are required.")
        try:
            recommendations = recommend_articles(user_activities)
            return JsonResponse(recommendations, safe=False)
        except Exception as e:
            return HttpResponseServerError(str(e))
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
# @api_view(["POST"])    
# def save_result(request):
#         if request.method == 'POST':
#             title_data = request.POST.get('title')
#             desc_data = request.POST.get('desc')
            