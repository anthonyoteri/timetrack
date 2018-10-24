from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

import timers.services

from timetrack import theme

from .forms import ProjectForm, ProjectEditForm
from .models import Project


# Create your views here.


@login_required(login_url="/accounts/login")
def list_view(request):

    if not Project.objects.filter(user=request.user).count():
        return redirect("projects:create")

    projects = (
        Project.objects.filter(user=request.user, archived="archived" in request.GET)
        .order_by("created")
        .all()
    )

    # Get the active timer to display the card
    active = timers.services.get_active_timer(request.user)

    return render(
        request,
        "projects/list.html",
        theme.apply({"projects": projects, "timer": active}),
    )


@login_required(login_url="/accounts/login")
def create_view(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("projects:list")
    else:
        form = ProjectForm()
    return render(request, "projects/create.html", theme.apply({"form": form}))


@login_required(login_url="/accounts/login")
def edit_view(request, slug):

    instance = Project.objects.get(user=request.user, slug=slug)

    if request.method == "POST":
        form = ProjectEditForm(instance=instance, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects:list")
    else:
        form = ProjectEditForm(instance=instance)
    return render(
        request, "projects/edit.html", theme.apply({"form": form, "project": instance})
    )


@login_required
def archive_view(request, slug):
    if request.method == "POST":
        instance = Project.objects.get(user=request.user, slug=slug)
        instance.archived = not instance.archived
        instance.save()

        if "next" in request.POST:
            return redirect(request.POST.get("next"))
    return redirect("projects:list")


@login_required(login_url="/accounts/login")
def delete_view(request, slug):
    if request.method == "POST":
        Project.objects.get(user=request.user, slug=slug).delete()

        if "next" in request.POST:
            return redirect(request.POST.get("next"))
    return redirect("projects:list")
