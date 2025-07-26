from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField

from .models import Student


class StudentForm(UserCreationForm):
    
    # captcha
    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
    )

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "captcha",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()

            if not Student.objects.filter(user=user).exists():
                Student.objects.create(
                    user=user,
                    name=self.cleaned_data["first_name"],
                    last_name=self.cleaned_data["last_name"],
                   
                )
                assign_group = Group.objects.get(name="student_team")
                user.groups.add(assign_group)

        return user
