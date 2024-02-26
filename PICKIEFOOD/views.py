from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Infos
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse


from openai import OpenAI
import openai

from datetime import datetime
import requests
import json

def index(request):
    if Infos.objects.count() != 0:
        return HttpResponseRedirect(reverse('sugg')) 
    else:
        return HttpResponseRedirect(reverse('form')) 

def form(request):
    return render(request, 'PICKIEFOOD/index.html')

def log(request):

    if Infos.objects.count() == 0:
        infos = Infos()
    else:
        infos = get_object_or_404(Infos, pk=1)

    print(request.POST)
    infos.name = request.POST['demo-name']
    infos.dob = request.POST['demo-date']
    infos.nation = request.POST['demo-nation']
    infos.gender = request.POST.get('demo-gender')
    infos.religon = request.POST['demo-religon']
    infos.dietary = request.POST['demo-pref']
    infos.height = request.POST['demo-height']
    infos.weight = request.POST['demo-weight']
    infos.aim = request.POST['demo-aim']
    infos.illness = ",".join(request.POST.getlist('demo-ill'))
    infos.allergen = ",".join(request.POST.getlist('demo-all'))

    infos.save()

    response_data = {'success': True, 'message': '数据已成功保存', 'redirect_url': reverse('sugg')}
        
    return JsonResponse(response_data)
    

def sugg(request):

    meal = 'breakfast'
    
    hour = datetime.now().hour

    if hour < 8:  # 早饭时间
        meal="breakfast"
    elif hour < 14:  # 午饭时间
        meal="lunch"
    elif hour < 24:  # 晚饭时间
        meal="dinner"


    Prompt  = "I am"
    infos = get_object_or_404(Infos, pk=1)
    if infos.name != "":
        Prompt += f" {infos.name},"
    if infos.dob != "":
        Prompt += f" {2024 - int(infos.dob.split('-')[0])} years old,"
    if infos.nation != "":
        Prompt += f" from {infos.nation},"
    if infos.gender != "":
        Prompt += f" {infos.gender},"
    if infos.height != "":
        Prompt += f" {infos.height} cm tall,"
    if infos.weight != "":
        Prompt += f" {infos.weight} kg in weight,"
    if infos.religon != "":
        Prompt += f" believe in {infos.religon},"
    if infos.dietary != "":
        Prompt += f" I am {infos.dietary},"
    if infos.illness != "":
        Prompt += f" I have {infos.illness},"
    if infos.allergen != "":
         Prompt += f" I am allergy to {infos.allergen}."
    if infos.aim!= "":
        Prompt += f" I want to {infos.aim}."

    Prompt += f"Please recommend me {meal}. Please return it in the json format of {{dishName:'', duration:'', ingredients: '', recipe: ''}} without any other content."

    print(Prompt)

    # with open('C:/api.txt') as f:
    #         AK=f.read()
    AK = ''

    client = OpenAI(
        api_key = AK
    )

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a dietary assistant who specializes in helping create healthy eating plans."},
            {"role": "user", "content": Prompt}
        ]
    )

    feedback = completion.choices[0].message.content
    print(feedback)
    feedback = feedback.replace('\n', '')
    feedback = feedback[feedback.find('{'): feedback.rfind('}') + 1]
    print(feedback)
    context = json.loads(feedback)
    print(context)

    # picPrompt = f"Give me a picture of {context['dishName']}."
    # picPrompt = f"I need a 3-step recipe to teach me how to cook it. Please show me the tutorial with only 3 separate pictures in the format of jpg without any other content. You don't need to summarize your results"

    # completion = client.chat.completions.create(
    #     model="gpt-4-turbo-preview",
    #     messages=[
    #         {"role": "system", "content": "You are a dietary assistant who specializes in helping create healthy eating plans."},
    #         {"role": "user", "content": picPrompt}
    #     ]
    # )

    # print(completion.choices[0].message)

    UNSPLASH_ACCESS_KEY = 'AhhKZrgAd7tzlOOBGNP7W8gyHiRAgOZntXYojIBlEPk'
    search_query = context['dishName']
    base_url = "https://api.unsplash.com"
    search_endpoint = "/search/photos"
    params = {
        'query': search_query,
        'per_page': 10,  # 设置每页返回的结果数量
    }
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    response = requests.get(base_url + search_endpoint, params=params, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        first_photo = data['results'][0]
        print(f"Photo by {first_photo['user']['name']}:")
        print(f"图片链接: {first_photo['links']['html']}")
        print(f"下载链接: {first_photo['links']['download']}")
    else:
        print("请求失败，状态码:", response.status_code)

    context['imgSrc'] = first_photo['links']['download']

    return render(request, 'PICKIEFOOD/food.html', context)

def img(request):
    image_data = request.FILES.get('image')
    print(image_data)

    response = openai.Vision.preview(image_data=image_data)

    print(response.predictions.keys())

    response_data = {'success': True, 'message': '数据已成功保存', 'redirect_url': reverse('sugg')}
        
    return JsonResponse(response_data)