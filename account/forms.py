from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm, UserCreationForm as BaseUserCreationForm, UsernameField

from .models import User, ServiceProvider, Category

class RegisterForm(forms.Form):

    username = UsernameField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"})
    )

    confirm_password = forms.CharField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"})
    )

    first_name = forms.CharField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    phone_number = forms.CharField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        required=True,
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.EmailInput(attrs={"class": "form-control", "type": "email"})
    )

    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control", "type": "file"})
    )

    is_service_provider = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "type": "checkbox"})
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "phone_number", "email", "avatar", "first_name", "last_name"]


class EditServiceProviderForm(forms.ModelForm):

    work = forms.CharField(
        required=True,
        label="Métier",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    town = forms.ChoiceField(
        choices=ServiceProvider.TOWNS,
        required=True,
        label="Ville",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 200px"})
    )

    level_of_education = forms.ChoiceField(
        choices=ServiceProvider.LEVEL_OF_EDUCATION,
        required=True,
        label="Niveau d'éducation",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 200px"})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Categorie de métier",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 200px"})
    )

    description = forms.CharField(
        required=True,
        label="Description",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "5"})
    )

    class Meta:
        model = ServiceProvider
        fields = ["work", "category", "town", "level_of_education", "description"]