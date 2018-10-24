from datetime import datetime, timezone

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import pendulum

from projects.models import Project

from timetrack import theme

from .forms import TimerForm
from .models import Timer
from . import services

# Create your views here.


@login_required(login_url="/accounts/login")
def list_view(request):

    try:
        begin = pendulum.parse(request.GET.get("from"))
    except TypeError:
        begin = None

    try:
        end = pendulum.parse(request.GET.get("to"))
    except TypeError:
        end = None

    query = Timer.objects.filter(project__user=request.user).order_by("-start")

    if begin:
        print(f"Got begin {begin}")
        query = query.filter(start__gte=begin)

    if end:
        print(f"Got end {end}")
        query = query.filter(start__lte=end)

    timers = query.all()

    return render(request, "timers/list.html", theme.apply({"timers": timers}))


@login_required(login_url="/accounts/login")
def edit_view(request, id):

    instance = Timer.objects.get(id=id)

    if request.method == "POST":
        form = TimerForm(user=request.user, instance=instance, data=request.POST)
        if form.is_valid():
            form.save()

            if "next" in request.POST:
                return redirect(request.POST.get("next"))

            return redirect("timers:list")
    else:
        form = TimerForm(user=request.user, instance=instance)
    return render(
        request, "timers/edit.html", theme.apply({"form": form, "timer": instance})
    )


@login_required(login_url="/accounts/login")
def create_view(request):

    if request.method == "POST":
        form = TimerForm(user=request.user, data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            active = services.get_active_timer(request.user)
            if active is not None and instance.start > active.start:
                active.stop = instance.start
                active.save()
            instance.save()

            if "next" in request.POST:
                return redirect(request.POST.get("next"))

            return redirect("timers:list")
    else:
        form = TimerForm(user=request.user)
    return render(request, "timers/create.html", theme.apply({"form": form}))


@login_required(login_url="/accounts/login")
def delete_view(request, id):
    if request.method == "POST":
        Timer.objects.get(id=id).delete()
        if "next" in request.POST:
            return redirect(request.POST.get("next"))

    return redirect("timers:list")


@login_required(login_url="/accounts/login")
def stop_view(request, id):
    if request.method == "POST":
        timer = Timer.objects.get(id=id)
        timer.stop = datetime.now(timezone.utc)
        timer.save()

        print(f"Got data {request.POST}")

        if "next" in request.POST:
            return redirect(request.POST.get("next"))

    return redirect("timers:list")


@login_required(login_url="/accounts/login")
def start_view(request, slug):
    if request.method == "POST":
        project = Project.objects.get(slug=slug)
        form = TimerForm(
            user=request.user,
            data={"project": project.id, "start": datetime.now(timezone.utc)},
        )

        if form.is_valid():
            form.save()

            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            return redirect("timers:list")

    return redirect("timers:list")
