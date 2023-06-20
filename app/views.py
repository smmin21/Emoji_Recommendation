from django.shortcuts import render, redirect
from .apps import AppConfig
from django.http import JsonResponse
import json

def home(request):
    if (request.method == 'POST'):
        jsonData = json.loads(request.body)
        input_txt = jsonData.get('body')
        result_df = AppConfig.model.find_emoji(input_txt)
        result = result_df['emoji'].tolist()
        ctx = {'result': result}
        print(result)
        return JsonResponse(ctx)
    return render(request, 'home.html')
