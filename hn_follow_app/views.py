import json, math
from django.http import HttpResponseRedirect
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
            # check to see if the HN user is already in the database, if so add this user to it
            try:
                hn_user = HnUser.objects.get(username=form.cleaned_data["username"])
                hn_user.user.add(request.user)
                hn_user.save()
            except HnUser.DoesNotExist:
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
                hn_user.user.add(request.user)

            return HttpResponseRedirect("/users")
    else:
        form = HnUserForm()

    hn_users = HnUser.objects.filter(user=request.user).all()

    context = {
        "hn_users": hn_users,
        "may_add_more": True,
        "max_note_length": 200,
        "form": form,
    }

    return render(request, "hn_follow_app/hn_user_index.html", context)


@login_required
def hn_user_edit(request, username):
    hn_user = HnUser.objects.get(username=username)

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
    }

    return render(request, "hn_follow_app/hn_user_edit.html", context)


@login_required
def hn_user_delete(request, username):
    if request.method == "POST":
        hn_user = HnUser.objects.get(username=username)
        hn_user.delete()
        return HttpResponseRedirect("/users")

    context = {
        "username": username,
    }

    return render(request, "hn_follow_app/hn_user_delete.html", context)
