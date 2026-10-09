from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from .models import Cycle, Session, Text


class LandingView(TemplateView):
    template_name = "seminar/landing.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["next_session"] = Session.objects.filter(date__gte=timezone.now()).order_by("date").first()
        ctx["current_cycle"] = Cycle.objects.first()
        ctx["recent_sessions"] = Session.objects.filter(published=True)[:3]
        ctx["contact_email"] = getattr(settings, "SEMINAR_CONTACT_EMAIL", "")
        return ctx


class SessionListView(ListView):
    template_name = "seminar/session_list.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return Session.objects.filter(published=True).select_related("cycle")


class TextListView(ListView):
    template_name = "seminar/text_list.html"
    context_object_name = "texts"
    queryset = Text.objects.prefetch_related("editions")


def session_detail(request, cycle_slug, number):
    from django.shortcuts import render
    session = get_object_or_404(Session, cycle__slug=cycle_slug, number=number, published=True)
    previous = Session.objects.filter(cycle=session.cycle, number__lt=number, published=True).order_by("-number").first()
    following = Session.objects.filter(cycle=session.cycle, number__gt=number, published=True).order_by("number").first()
    return render(request, "seminar/session_detail.html", {"session": session, "previous": previous, "following": following})
