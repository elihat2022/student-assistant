# forms.py
from django import forms
from django.forms.models import inlineformset_factory

from .models import Keywords, Subject, Transcription
from taggit.managers import TaggableManager

class PatientForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["subject_name"]


class MedicHistoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))
    subject_name = forms.CharField(max_length=100)
   
    class Meta:
        model = Transcription
        fields = ["subject_name", "name", "tags", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.subject:
            self.fields["subject_name"].initial = self.instance.subject.subject_name


class TreatmentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 1}), label="")

    class Meta:
        model = Keywords
        fields = ["description"]


TreatmentFormSet = inlineformset_factory(
    Transcription, Keywords, form=TreatmentForm, extra=1, can_delete=True
)


# Search
class SearchForm(forms.Form):
    query = forms.CharField()
    

class TranscriptionFilter(forms.Form):
    tag = TaggableManager()