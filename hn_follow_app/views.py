import requests
from django.shortcuts import render
from .models import HnUser

def index(request):
    # Get all HN users
    hn_users = HnUser.objects.order_by('username')
    hn_user_details = {}
    for hn_user in hn_users:
        details = requests.get('https://hacker-news.firebaseio.com/v0/user/'+hn_user.username+'.json')
        hn_user_details[hn_user.username] = details.json()

    context = {'hn_users': hn_user_details}

    return render(request, 'hn_follow_app/index.html', context)