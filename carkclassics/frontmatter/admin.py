from django.contrib import admin

from .models import Cycle, Edition, Session, Text


class EditionInline(admin.StackedInline):
    model = Edition
    extra = 1


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "tradition", "order")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EditionInline]


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "start_date")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("cycle", "number", "passage", "date", "published")
    list_filter = ("cycle", "published")
    fieldsets = (
        ("Schedule", {"fields": ("cycle", "number", "date", "venue", "venue_address", "passage", "assignment_for_next")}),
        ("Minutes (anonymous)", {"fields": ("published", "headcount", "opening_question", "summary", "unresolved", "facilitator_note")}),
    )