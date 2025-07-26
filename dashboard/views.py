from account.models import Student
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

# views.py
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import UpdateView
from openai import OpenAI

from .forms import (
    VoiceNoteForm,
    Subject,
    DescriptionFormSet,
    SearchForm,
    TranscriptionFilter,
)
from .models import Subject, Transcription
from .tasks import transcribe_audio
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_http_methods
#Search
from django.contrib.postgres.search import (
    SearchVector)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def home(request):
    return render(request, "dashboard/home.html")

@ratelimit(key='ip', rate='50/d')
@login_required(login_url="/account/login")
def Record_View(request):
    if request.method == "POST":
        return handle_post_request(request)
    elif request.method == "GET":
        return render(request, "dashboard/recording.html")
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def handle_post_request(request):
    subject_name = request.POST.get("subject_name")
    tags = request.POST.get("tag")

    if not subject_name:
        return JsonResponse({"error": "Subject name is required"}, status=400)

    subject_instance = Subject.objects.create(subject_name=subject_name)

    if "voice_input" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    audio_file = request.FILES["voice_input"]
    user_id = request.user.id

    # Retrieve the Doctor instance using the doctor_id
    try:
        student_instance = Student.objects.get(user_id=user_id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)

    audio_instance = Transcription.objects.create(
        audio=audio_file, subject=subject_instance, student=student_instance, tags=tags
    )
    
    audio_url = audio_instance.audio.url  # Obtener la URL del archivo
    audio_instance.audio_url = audio_url
    #print(audio_instance.audio_url)# Guardar la URL en el modelo
    transcription_task = transcribe_audio.delay(
        audio_url, audio_instance.id
    )  # Call the Celery task to transcribe the audio

    return redirect(reverse("transcriptions"))

class Transcription_List(LoginRequiredMixin, ListView):
    login_url = "account/login"
    model = Transcription

    fields = ["subject", "audio", "created"]
    ordering = ["-created"]
    template_name = "dashboard/transcription/transcription_list.html"
    context_object_name = "transcription_list"

    def get_queryset(self):
        
        student = self.request.user.student

        return Transcription.objects.filter(student=student)


class Transcription_Detail(LoginRequiredMixin, DetailView):
    login_url = "account/login"
    model = Transcription
    template_name = "dashboard/transcription/transcription_detail.html"
    context_object_name = "transcription"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        if pk is None:
            return None  # Handle case where ID is missing
        return get_object_or_404(Transcription, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transcription = self.get_object()
        if transcription:
            context["transcription"] = transcription
        return context


class UpdateTranscriptionDetail(LoginRequiredMixin, UpdateView):
    model = Transcription
    form_class = VoiceNoteForm
    template_name = "dashboard/transcription/transcription_update.html"

    def get_success_url(self):
        return reverse_lazy("transcriptions")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["treatment_formset"] = DescriptionFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["treatment_formset"] = DescriptionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        treatment_formset = context["treatment_formset"]
        if form.is_valid() and treatment_formset.is_valid():
            # Actualizar el nombre del paciente
            subject_name = form.cleaned_data["subject_name"]
            self.object.subject.subject_name = subject_name
            self.object.subject.save()

            self.object = form.save()
            treatment_formset.instance = self.object
            treatment_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class DeleteTranscription(LoginRequiredMixin, DeleteView):
    model = Transcription
    template_name = "dashboard/transcription/transcription_delete.html"
    success_url = reverse_lazy("transcriptions")


@require_http_methods(["GET"])
def transcription_search(request):
    search_text = request.GET.get('search', '').strip()
    if search_text:
        results = (
            Transcription.objects.annotate(
                subject_similarity=TrigramSimilarity(
                    "subject__subject_name", search_text
                ),
                # Si tags es un campo TextField o CharField
                description_similarity=TrigramSimilarity("description", search_text),
                similarity=Greatest(
                    "subject_similarity",
                    "description_similarity",
                ),
            )
            .filter(similarity__gt=0.3)
            .order_by("-similarity")
        )
    else:
        results = []
    
    return render(
        request,
        "dashboard/partials/search_results.html",
        context={'results': results}
    )
