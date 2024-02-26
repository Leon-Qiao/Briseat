from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Infos
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse


from openai import OpenAI


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
    infos.gender = request.POST['demo-gender']
    infos.religon = request.POST['demo-religon']
    infos.dietary = request.POST['demo-pref']
    infos.height = request.POST['demo-height']
    infos.weight = request.POST['demo-weight']
    infos.illness = ",".join(request.POST.getlist('demo-ill'))
    infos.allergen = ",".join(request.POST.getlist('demo-all'))

    infos.save()

    response_data = {'success': True, 'message': '数据已成功保存', 'redirect_url': reverse('sugg')}
        
    return JsonResponse(response_data)
    

def sugg(request):

    meal = 'breakfast'

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

    # if infos.aims != "":
    #     Prompt += f" I want to {infos.aims}."

    Prompt += f"Please recommend me {meal}. Please return it in the json format of {{dishName:'', duration:'', ingredients: []}}."

    print(Prompt)

    client = OpenAI(
        api_key='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'
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a dietary assistant who specializes in helping create healthy eating plans."},
            {"role": "user", "content": Prompt}
        ]
    )

    print(completion.choices[0].message)

    return render(request, 'PICKIEFOOD/food.html')





