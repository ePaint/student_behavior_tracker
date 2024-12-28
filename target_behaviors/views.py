from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from target_behaviors.models import (
    TargetBehavior,
    TargetBehaviorWeek,
    TargetBehaviorRecord,
)


class Detail(DetailView):
    template_name = "target_behaviors/detail.html"
    url_name = "target-behaviors-detail"
    model = TargetBehavior
    context_object_name = "target_behavior"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weeks"] = TargetBehaviorWeek.objects.filter(
            user=self.request.user, target_behavior=self.object
        )
        context["current_points"] = sum(
            [week.current_points for week in context["weeks"]]
        )
        context["current_percentage"] = int(
            context["current_points"] / self.object.max_points * 100 + 0.5
        )
        context["chart_labels"] = [f"W{week.week_number}" for week in context["weeks"]]
        context["chart_points"] = [week.current_points for week in context["weeks"]]
        return context


def _get_week_records(request, target_behavior, week):
    records = {}
    for day in target_behavior.days.all():
        records[day] = {}
        for period in target_behavior.periods.all():
            records[day][period] = TargetBehaviorRecord.objects.get_or_create(
                user=request.user,
                target_behavior=target_behavior,
                week=week,
                day=day,
                period=period,
            )[0]
    return records


def _handle_week_form(request):
    target_behavior = TargetBehavior.objects.get(
        uuid=request.POST.get("target_behavior_uuid")
    )
    week = TargetBehaviorWeek.objects.get_or_create(
        week_number=request.POST.get("week_number", 1),
        user=request.user,
        target_behavior=target_behavior,
    )[0]
    for key, value in request.POST.items():
        if key.startswith("value_"):
            record_id = key.split("_")[1]
            record = TargetBehaviorRecord.objects.get(pk=record_id)
            record.value = value
            notes = request.POST.get(f"notes_{record_id}")
            record.notes = notes
            record.save()
    return week


@login_required
def create_target_behavior_week(request):
    if request.method == "POST":
        week = _handle_week_form(request)
        return redirect("target-behaviors-week-edit", slug=week.uuid)

    # GET request
    target_behavior_uuid = request.GET.get("target_behavior_uuid")
    if not target_behavior_uuid:
        return HttpResponse("Target Behavior ID is required", status=400)
    target_behavior = TargetBehavior.objects.get(uuid=target_behavior_uuid)
    week_count = TargetBehaviorWeek.objects.filter(
        user=request.user, target_behavior=target_behavior
    ).count()
    week = TargetBehaviorWeek.objects.get_or_create(
        week_number=week_count + 1,
        user=request.user,
        target_behavior=target_behavior,
    )[0]

    return render(
        request,
        "target_behaviors/week_form.html",
        {
            "week": week,
            "records": _get_week_records(request, target_behavior, week),
            "options": [option[0] for option in TargetBehaviorRecord.VALUE_CHOICES],
        },
    )


@login_required
def edit_target_behavior_week(request, slug):
    if request.method == "POST":
        week = _handle_week_form(request)
        return redirect("target-behaviors-week-edit", slug=week.uuid)

    # GET request
    week = TargetBehaviorWeek.objects.get(uuid=slug)
    return render(
        request,
        "target_behaviors/week_form.html",
        {
            "week": week,
            "records": _get_week_records(request, week.target_behavior, week),
            "options": [option[0] for option in TargetBehaviorRecord.VALUE_CHOICES],
        },
    )
