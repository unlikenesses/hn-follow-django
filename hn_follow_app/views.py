import json, math
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import HnUser
from .forms import AddHnUserForm
from .hn_service import HnService


def index(request):
    page = request.GET.get("page", 1)
    return render(
        request,
        "hn_follow_app/index.html",
        {
            "page": page,
        },
    )


def submissions(request):
    page = int(request.GET.get("page", 1))
    perPage = 5

    hn_service = HnService()

    # Get all HN users submission IDs, sorted
    hn_users = HnUser.objects.values_list("username", flat=True)
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


def hn_user_index(request):
    if request.method == "POST":
        form = AddHnUserForm(request.POST)
        if form.is_valid():
            hn_service = HnService()
            # try to get the HN user from the HN API
            user_from_api = hn_service.getHnUserDetailsFromAPI(
                form.cleaned_data["username"]
            )
            if user_from_api is None:
                raise Exception("User not found")
            # add the user
            submissions = json.dumps(user_from_api["submitted"])
            hn_user = HnUser(
                username=form.cleaned_data["username"],
                about=user_from_api.get("about"),
                karma=user_from_api["karma"],
                submissions=submissions,
                notes=form.cleaned_data["notes"],
            )
            hn_user.save()

            return HttpResponseRedirect("users")
    else:
        form = AddHnUserForm()

    hn_users = HnUser.objects.all()

    context = {
        "hn_users": hn_users,
        "may_add_more": True,
        "max_note_length": 200,
        "form": form,
    }

    return render(request, "hn_follow_app/hn_user_index.html", context)


def hn_user_delete(request, username):
    if request.method == "POST":
        hn_user = HnUser.objects.get(username=username)
        hn_user.delete()
        return HttpResponseRedirect("/users")

    context = {
        "username": username,
    }

    return render(request, "hn_follow_app/hn_user_delete.html", context)
