import math
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HnUser
from .forms import HnUserForm
from .hn_service import HnService


@login_required
def index(request):
    page = request.GET.get("page", 1)
    return render(
        request,
        "hn_follow_app/index.html",
        {
            "page": page,
            "current": "index",
        },
    )


@login_required
def submissions(request):
    page = int(request.GET.get("page", 1))
    perPage = 5

    hn_service = HnService()

    # Get all HN users submission IDs, sorted
    hn_users = HnUser.objects.filter(user=request.user).values_list(
        "username", flat=True
    )
    submitted = hn_service.getAllSubmitted(hn_users)
    numSubmitted = len(submitted)
    numPages = math.ceil(numSubmitted / perPage)
    offset = (page - 1) * perPage
    subset = submitted[offset : offset + perPage]
    submissions = hn_service.getSubmissions(subset)

    prev = None
    if page > 1:
        prev = page - 1

    next = None
    if page < numPages:
        next = page + 1

    context = {
        "submissions": submissions,
        "link_url": "https://news.ycombinator.com/item?id=",
        "page": page,
        "prev": prev,
        "next": next,
        "numPages": numPages,
    }

    return render(request, "hn_follow_app/submissions.html", context)


@login_required
def hn_user_index(request):
    if request.method == "POST":
        form = HnUserForm(request.POST)
        if form.is_valid():
            hn_service = HnService()
            hn_service.addHnUserToUser(form.cleaned_data, request.user)

            return HttpResponseRedirect("/users")
    else:
        form = HnUserForm()

    hn_users = HnUser.objects.filter(user=request.user).all()

    context = {
        "hn_users": hn_users,
        "may_add_more": True,
        "max_note_length": 200,
        "form": form,
        "current": "users",
    }

    return render(request, "hn_follow_app/hn_user_index.html", context)


@login_required
def hn_user_edit(request, username):
    hn_user = HnUser.objects.get(username=username)
    if not hn_user.user.filter(username=request.user).exists():
        raise Http404

    if request.method == "POST":
        form = HnUserForm(instance=hn_user, data=request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/users")
    else:
        form = HnUserForm(instance=hn_user)

    context = {
        "username": username,
        "form": form,
        "current": "users",
    }

    return render(request, "hn_follow_app/hn_user_edit.html", context)


@login_required
def hn_user_delete(request, username):
    hn_user = HnUser.objects.get(username=username)
    if not hn_user.user.filter(username=request.user).exists():
        raise Http404
    if request.method == "POST":
        hn_user.delete()
        return HttpResponseRedirect("/users")

    context = {
        "username": username,
        "current": "users",
    }

    return render(request, "hn_follow_app/hn_user_delete.html", context)
