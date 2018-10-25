import collections
from datetime import datetime, timedelta
import pendulum

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from timetrack import theme
from timers.models import Timer

# Create your views here.


@login_required(login_url="/accounts/login")
def view_day(request):

    begin = pendulum.parse(request.GET.get("date", pendulum.today().isoformat()))

    end = begin.add(days=1)
    timers = (
        Timer.objects.filter(
            project__user=request.user,
            start__gt=_sql_time(begin),
            start__lt=_sql_time(end),
        )
        .order_by("start")
        .all()
    )

    context = {
        "begin": begin,
        "summary": dict(_make_summary(timers)),
        "records": timers,
        "next": end,
        "prev": begin.subtract(days=1),
    }

    return render(request, "reports/day.html", theme.apply(context))


@login_required(login_url="/accounts/login")
def view_week(request):

    begin = pendulum.parse(
        request.GET.get("date", pendulum.today().isoformat())
    ).start_of("week")
    end = begin.add(weeks=1)
    timers = (
        Timer.objects.filter(
            project__user=request.user,
            start__gt=_sql_time(begin),
            start__lt=_sql_time(end),
        )
        .order_by("start")
        .all()
    )

    weekly_summary = _make_summary(timers)
    daily_summary = _make_daily_summary(
        timers, sorted(weekly_summary["data"].keys()), begin, end
    )

    context = {
        "begin": begin,
        "end": end.subtract(days=1),
        "weekly_summary": weekly_summary,
        "daily_summary": [daily_summary],
        "records": timers,
        "next": end,
        "prev": begin.subtract(weeks=1),
    }

    return render(request, "reports/week.html", theme.apply(context))


@login_required(login_url="/accounts/login")
def view_month(request):
    begin = pendulum.parse(
        request.GET.get("date", pendulum.today().isoformat())
    ).start_of("month")
    end = begin.add(months=1)
    timers = (
        Timer.objects.filter(
            project__user=request.user,
            start__gt=_sql_time(begin),
            start__lt=_sql_time(end),
        )
        .order_by("start")
        .all()
    )

    daily_summary = []
    for week_begin in list((end - begin).range("weeks"))[:-1]:
        week_end = week_begin.add(weeks=1)

        timers = (
            Timer.objects.filter(
                project__user=request.user,
                start__gt=_sql_time(week_begin),
                start__lt=_sql_time(week_end),
            )
            .order_by("start")
            .all()
        )
        if not timers:
            continue

        weekly_summary = _make_summary(timers)
        daily_summary.append(
            _make_daily_summary(
                timers, sorted(weekly_summary["data"].keys()), week_begin, week_end
            )
        )

    context = {
        "begin": begin,
        "end": end.subtract(days=1),
        "daily_summary": daily_summary,
        "next": end,
        "prev": begin.subtract(months=1),
    }

    return render(request, "reports/month.html", theme.apply(context))


def _sql_time(ts: pendulum.DateTime) -> datetime:
    dt = datetime.fromtimestamp(int(ts.timestamp()))
    dt.replace(tzinfo=ts.timezone)
    return dt


def _make_summary(timers):
    weekly_summary_data = collections.defaultdict(timedelta)
    for timer in timers:
        weekly_summary_data[timer.project.name] += timedelta(
            seconds=timer.elapsed.seconds
        )

    weekly_summary_total = timedelta(
        seconds=sum([v.total_seconds() for _, v in weekly_summary_data.items()])
    )
    return {"data": dict(weekly_summary_data), "total": weekly_summary_total}


def _make_daily_summary(timers, projects, begin, end):

    daily_summary_data = collections.defaultdict(list)

    for project in projects:
        for day in list((end - begin).range("days"))[:-1]:
            timer_set = {
                t
                for t in timers
                if day <= t.start < day.add(days=1) and t.project.name == project
            }
            s = sum(t.elapsed.seconds for t in timer_set) if timer_set else 0
            daily_summary_data[project].append(timedelta(seconds=s))

    daily_summary_totals = [
        timedelta(seconds=s)
        for s in [
            sum([v.total_seconds() for v in l])
            for l in list(zip(*daily_summary_data.values()))
        ]
    ]
    daily_summary_labels = [
        d.format("dddd") for d in list((end - begin).range("days"))[:-1]
    ]
    return {
        "begin": begin,
        "end": end.subtract(days=1),
        "data": dict(daily_summary_data),
        "totals": daily_summary_totals or [""] * len(list((end - begin).range("days"))),
        "labels": daily_summary_labels,
    }
