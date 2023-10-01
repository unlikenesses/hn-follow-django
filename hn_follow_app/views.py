from django.shortcuts import render
from .models import HnUser
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