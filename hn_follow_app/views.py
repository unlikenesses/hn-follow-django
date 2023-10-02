import json, ast
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import HnUser
from .forms import AddHnUserForm
from .hn_service import HnService

def index(request):
    hn_service = HnService()

    # Get all HN users submission IDs, sorted
    hn_users = HnUser.objects.values_list('username', flat=True)
    submitted = hn_service.getAllSubmitted(hn_users)
    # raise Exception(submitted)

    # Get last x submissions from this list
    subset = submitted[:10]
    # subset = [37705848, 37702627, 37699954, 37699861, 37695169, 37672860, 37672803, 37665865, 37665845, 37659329]
    submissions = hn_service.getSubmissions(subset)

    context = {
        'submissions': submissions,
        'link_url': 'https://news.ycombinator.com/item?id=',
    }

    return render(request, 'hn_follow_app/index.html', context)

def hn_user_index(request):
    if request.method == 'POST':
        form = AddHnUserForm(request.POST)
        if form.is_valid():
            hn_service = HnService()
            # try to get the HN user from the HN API
            user_from_api = hn_service.getHnUserDetailsFromAPI(form.cleaned_data['username'])
            if user_from_api is None:
                raise Exception('User not found')
            # add the user
            submissions=json.dumps(user_from_api['submitted'])
            hn_user = HnUser(
                username=form.cleaned_data['username'],
                about=user_from_api.get('about'),
                karma=user_from_api['karma'],
                submissions=submissions,
                notes=form.cleaned_data['notes'], 
            )
            hn_user.save()

            return HttpResponseRedirect('users')
    else:
        form = AddHnUserForm()

    hn_users = HnUser.objects.all()

    context = {
        'hn_users': hn_users,
        'may_add_more': True,
        'max_note_length': 200,
        'form': form,
    }

    return render(request, 'hn_follow_app/hn_user_index.html', context)
