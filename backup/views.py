import gzip
import tempfile
import urllib.parse

import pendulum

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from timetrack import theme

from projects.models import Project
from timers.models import Timer


@login_required(login_url="/accounts/login")
def index_view(request):

    return render(request, "backup/index.html", theme.apply({}))


@login_required(login_url="/accounts/login")
def backup_view(request):
    projects = Project.objects.filter(user=request.user)

    project_csv = []
    for project in projects:
        project_csv.append(
            ",".join(
                map(
                    str,
                    [
                        type(project).__name__,
                        urllib.parse.quote(project.name),
                        project.slug,
                        urllib.parse.quote(project.description),
                        project.archived,
                        project.favorite,
                        project.created.isoformat(),
                        project.last_updated.isoformat(),
                    ],
                )
            )
        )

    timers = Timer.objects.filter(project__user=request.user)
    timer_csv = []
    for timer in timers:
        timer_csv.append(
            ",".join(
                map(
                    str,
                    [
                        type(timer).__name__,
                        timer.project.slug,
                        timer.start.isoformat(),
                        timer.stop.isoformat() if timer.stop else "",
                    ],
                )
            )
        )

    with tempfile.NamedTemporaryFile("r+b") as f:

        with gzip.open(f.name, "wb") as fgz:
            for line in project_csv:
                fgz.write(line.encode("UTF-8") + "\n".encode("UTF-8"))
            for line in timer_csv:
                fgz.write(line.encode("UTF-8") + "\n".encode("UTF-8"))

        f.flush()
        f.seek(0)

        response = HttpResponse(f.read(), content_type="application/gzip")
        response[
            "Content-Disposition"
        ] = f"inline; filename=timetrack_{request.user}_{pendulum.now().isoformat()}.csv.gz"
        return response


@login_required
def restore_view(request):
    if request.method == "POST":

        if "dump_file" not in request.FILES:
            return render(
                request,
                "backup/index.html",
                theme.apply({"errors": ["You must select a file to restore"]}),
            )

        # Make sure all existing records are wiped
        Timer.objects.all().delete()
        Project.objects.all().delete()

        try:
            with gzip.open(request.FILES["dump_file"], "rb") as f:

                # Make sure all existing records are wiped
                Timer.objects.all().delete()
                Project.objects.all().delete()

                for line in map(lambda l: l.decode("UTF-8").strip(), f.readlines()):
                    fields = line.split(",")

                    cls = fields.pop(0)
                    if cls == "Project":
                        name, slug, description, archived, favorite, created, last_updated = (
                            fields
                        )

                        p = Project(
                            name=urllib.parse.unquote(name),
                            slug=slug,
                            description=urllib.parse.unquote(description),
                            archived=archived,
                            favorite=favorite,
                            created=pendulum.parse(created),
                            last_updated=pendulum.parse(last_updated),
                            user=request.user,
                        )
                        try:
                            p.save()
                        except IntegrityError:
                            continue

                    if cls == "Timer":
                        slug, start, stop = fields

                        project = Project.objects.get(slug=slug)

                        t = Timer(
                            project=project,
                            start=pendulum.parse(start),
                            stop=pendulum.parse(stop) if stop else None,
                        )

                        try:
                            t.save()
                        except IntegrityError:
                            continue

            return redirect("projects:list")
        except OSError:
            return render(
                request,
                "backup/index.html",
                theme.apply({"errors": ["Backup file is invalid!"]}),
            )
