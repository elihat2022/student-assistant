from django.contrib import admin

from .models import Keywords, Subject, Transcription


@admin.register(Transcription)
class History(admin.ModelAdmin):
    list_display = ["subject", "created"]
    search_fields = ["subject__subject_name"]


@admin.register(Subject)
class Subject_Case_Admin(admin.ModelAdmin):
    list_display = ["subject_name"]


@admin.register(Keywords)
class Treatment_Admin(admin.ModelAdmin):
    list_display = ["transcription_record"]
