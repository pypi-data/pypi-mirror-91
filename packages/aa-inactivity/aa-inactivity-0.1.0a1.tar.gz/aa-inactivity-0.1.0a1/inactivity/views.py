import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from .forms import CreateRequestForm
from .models import LeaveOfAbsence
from .utils import messages_plus


@login_required
@permission_required("inactivity.basic_access")
def index(request):

    context = {}
    return render(request, "inactivity/index.html", context)


@login_required
@permission_required("inactivity.manage_leave")
def manage(request):

    context = {}
    return render(request, "inactivity/manage.html", context)


@login_required
@permission_required("inactivity.basic_access")
def list_loa_requests(request):
    results = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for req in LeaveOfAbsence.objects.filter(
        Q(user=request.user), Q(end=None) | Q(end__gt=now)
    ):
        results.append(
            {
                "start": req.start,
                "end": req.end if req.end else "&mdash;",
                "approved": req.approver is not None,
                "pk": req.pk,
            }
        )

    return JsonResponse(results, safe=False)


@login_required
@permission_required("inactivity.manage_leave")
def list_pending_loa_requests(request):
    results = []
    now = datetime.datetime.now(datetime.timezone.utc)

    for req in LeaveOfAbsence.objects.filter(
        Q(end=None) | Q(end__gt=now), Q(approver=None)
    ):
        results.append(
            {
                "user": req.user.profile.main_character.character_name,
                "start": req.start,
                "end": req.end if req.end else "&mdash;",
                "approved": req.approver is not None,
                "pk": req.pk,
            }
        )

    return JsonResponse(results, safe=False)


@login_required
@permission_required("inactivity.manage_leave")
def approve_loa_request(request, request_id):
    req = LeaveOfAbsence.objects.get(pk=request_id)
    req.approver = request.user
    req.save()
    messages_plus.success(
        request,
        format_html(
            _("Your have appproved %(user)s's leave request.")
            % {
                "user": format_html(
                    "<strong>{}</strong>",
                    req.user.profile.main_character.character_name,
                ),
            }
        ),
    )
    return redirect("inactivity:manage_requests")


@login_required
@permission_required("inactivity.basic_access")
@require_POST
def cancel_loa_request(request, request_id):
    if request.user.has_perm("inactivity.manage_leave"):
        candidate = LeaveOfAbsence.objects.filter(pk=request_id).first()
    else:
        candidate = LeaveOfAbsence.objects.filter(
            user=request.user, pk=request_id
        ).first()
    if candidate:
        candidate.delete()
        messages_plus.info(
            request,
            format_html(
                _(
                    "Your leave of absence request from %(start)s to %(end)s has been deleted."
                )
                % {
                    "start": format_html("<strong>{}</strong>", candidate.start),
                    "end": format_html("<strong>{}</strong>", candidate.end),
                }
            ),
        )
        return redirect("inactivity:index")
    else:
        messages_plus.error(
            request,
            format_html(_("No leave of absence request matched your request.")),
        )
        return redirect("inactivity:index")


@login_required
@permission_required("inactivity.basic_access")
def create_loa_request(request):
    if request.method == "GET":
        create_form = CreateRequestForm()
        context = {"create_form": create_form}
        return render(request, "inactivity/create_loa.html", context)
    elif request.method == "POST":
        create_form = CreateRequestForm(request.POST)
        model = create_form.save(commit=False)
        model.user = request.user
        model.save()
        messages_plus.info(
            request,
            format_html(
                _(
                    "Your leave of absence request from %(start)s to %(end)s has been submitted for review."
                )
                % {
                    "start": format_html("<strong>{}</strong>", model.start),
                    "end": format_html("<strong>{}</strong>", model.end),
                }
            ),
        )
        return redirect("inactivity:index")
