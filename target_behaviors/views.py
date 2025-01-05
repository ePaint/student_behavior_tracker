from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from target_behaviors.models import (
    TargetBehavior,
    TargetBehaviorWeek,
    TargetBehaviorRecord,
)
from users.models import CustomUser


class Detail(DetailView):
    template_name = "target_behaviors/detail.html"
    url_name = "target-behaviors-detail"
    model = TargetBehavior
    context_object_name = "target_behavior"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = CustomUser.objects.get(
            uuid=self.request.resolver_match.kwargs.get("user_uuid")
        )
        context["weeks"] = TargetBehaviorWeek.objects.filter(
            user=context["user"], target_behavior=self.object
        )
        context["current_points"] = sum(
            [week.current_points for week in context["weeks"]]
        )
        context["current_max_points"] = self.object.max_points * len(context["weeks"])
        context["current_percentage"] = int(
            context["current_points"] / max(1, context["current_max_points"]) * 100
            + 0.5
        )
        context["goal_points"] = self.object.week_goal_points * len(context["weeks"])
        context["goal_max_points"] = self.object.max_points * len(context["weeks"])
        context["chart_labels"] = [f"W{week.week_number}" for week in context["weeks"]]
        context["chart_points"] = [
            week.current_points / week.target_behavior.max_points * 100
            for week in context["weeks"]
        ]
        return context


class Create(CreateView):
    template_name = "target_behaviors/create.html"
    url_name = "target-behaviors-create"
    fields = ["name", "description", "days", "periods", "week_goal_percentage"]
    model = TargetBehavior
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = CustomUser.objects.get(
            uuid=self.request.resolver_match.kwargs.get("user_uuid")
        )
        return context

    # execute after form is valid
    def form_valid(self, form):
        super().form_valid(form)
        user = CustomUser.objects.get(
            uuid=self.request.resolver_match.kwargs.get("user_uuid")
        )
        user.target_behaviors.add(self.object)
        user.save()
        if getattr(self.request.user, "level_of_access_granted") == "Teacher":
            return redirect("users-profile-other", slug=user.uuid)
        return redirect("users-profile")


class Edit(UpdateView):
    template_name = "target_behaviors/edit.html"
    url_name = "target-behaviors-edit"
    fields = ["name", "description", "days", "periods", "week_goal_percentage"]
    model = TargetBehavior
    slug_field = "uuid"
    context_object_name = "target_behavior"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = CustomUser.objects.get(
            uuid=self.request.resolver_match.kwargs.get("user_uuid")
        )
        return context

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(
            "target-behaviors-detail",
            slug=self.object.uuid,
            user_uuid=self.request.resolver_match.kwargs.get("user_uuid"),
        )


def delete_target_behavior(request, slug, user_uuid):
    target_behavior = TargetBehavior.objects.get(uuid=slug)
    user = CustomUser.objects.get(uuid=user_uuid)
    user.target_behaviors.remove(target_behavior)
    user.save()
    if getattr(request.user, "level_of_access_granted") == "Teacher":
        return redirect("users-profile-other", slug=user.uuid)
    return redirect("users-profile")


def _get_week_records(week):
    records = {}
    for day in week.target_behavior.days.all():
        records[day] = {}
        for period in week.target_behavior.periods.all():
            records[day][period] = TargetBehaviorRecord.objects.get_or_create(
                user=week.user,
                target_behavior=week.target_behavior,
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
        user=CustomUser.objects.get(uuid=request.POST.get("user_uuid")),
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
    user_uuid = request.GET.get("user_uuid")
    if not user_uuid:
        return HttpResponse("User ID is required", status=400)
    target_behavior = TargetBehavior.objects.get(uuid=target_behavior_uuid)
    user = CustomUser.objects.get(uuid=user_uuid)
    print(user.email)
    week_count = TargetBehaviorWeek.objects.filter(
        user=user, target_behavior=target_behavior
    ).count()
    week = TargetBehaviorWeek.objects.get_or_create(
        week_number=week_count + 1,
        user=user,
        target_behavior=target_behavior,
    )[0]

    return render(
        request,
        "target_behaviors/week_form.html",
        {
            "week": week,
            "records": _get_week_records(week),
            "options": [option[0] for option in TargetBehaviorRecord.VALUE_CHOICES],
        },
    )


@login_required
def edit_target_behavior_week(request, slug):
    if request.method == "POST":
        week = _handle_week_form(request)
        print(week.user.uuid)
        return redirect("target-behaviors-week-edit", slug=week.uuid)

    # GET request
    week = TargetBehaviorWeek.objects.get(uuid=slug)
    return render(
        request,
        "target_behaviors/week_form.html",
        {
            "week": week,
            "records": _get_week_records(week),
            "options": [option[0] for option in TargetBehaviorRecord.VALUE_CHOICES],
        },
    )
