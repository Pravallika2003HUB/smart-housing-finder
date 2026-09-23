from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    role = forms.ChoiceField(
        choices=[(User.STUDENT, "Student / Bachelor"), (User.OWNER, "Property Owner")],
        widget=forms.RadioSelect,
        initial=User.STUDENT,
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "phone", "role", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists. Please login.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.full_name = self.cleaned_data["full_name"]
        user.phone = self.cleaned_data["phone"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "phone"]
