from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import requests
import os,pickle

# Create your views here.
def index(request):
    return HttpResponse(f"{request} Text Summarizer index")


# @csrf_exempt
# @api_view(['POST'])
# def summarize(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#         response = requests.post('http://127.0.0.1:1112/summarize', json={'text': text})
#         if response.status_code == 200:
#             data = response.json()
#             return JsonResponse(data)
#         else:
#             return JsonResponse({'error': 'Failed to summarize'}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
@api_view(['POST'])
def summarize(request):
    if request.method == 'POST':
        try:
            text_data = request.data.get('text', '')
            file_path = os.path.abspath('text_summarizer/api/text.pkl')
            print(file_path)
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    model = pickle.load(f)

                result = model(text_data)[0]
                return JsonResponse({'result': result})
            else:
                return JsonResponse({'error': 'Model file not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for this view'})

