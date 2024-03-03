from django.shortcuts import render, HttpResponse
import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import requests
import os,pickle
import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)


# with open("fake_news/models/fake_news.pkl", "rb") as f:
#     model_data = pickle.load(f)

# tfidf_vectorizer = model_data['vectorizer']
# model = model_data['model']

# Create your views here.
def index(request):
    return HttpResponse("Fake News Index")

@csrf_exempt
@api_view(['POST'])
def detect_fake_news(request):
    # if request.method == 'POST':
    #     text = request.POST.get('text', '')
    #     response = requests.post('http://127.0.0.1:1111/check', json={'text': text})
    #     if response.status_code == 200:
    #         data = response.json()
    #         return JsonResponse(data)
    #     else:
    #         return JsonResponse({'error': 'Failed to check fake news'}, status=500)
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)


    if request.method == 'POST':
        try:
            text_data = request.POST.get('text', '')  # Assuming 'text' is passed in form data
            file_path = os.path.abspath('fake_news/api/fake_news.pkl')
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    model_data = pickle.load(f)
                tfidf_vectorizer = model_data['vectorizer']
                model = model_data['model']
                tfidf_features = tfidf_vectorizer.transform([text_data])
                result = model.predict(tfidf_features)

                # Convert NumPy array to a Python list
                result_list = result.tolist()

                return JsonResponse({'result': result_list})
            else:
                return JsonResponse({'error': 'Model file not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for this view'})
