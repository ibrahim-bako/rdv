from django import forms
from django.forms import BaseModelFormSet

from .models import Calendar, Appointment, Availability
from account.models import ServiceProvider, Category
from django.forms import formset_factory, modelformset_factory

class CreateAppointmentForm(forms.ModelForm):

    date = forms.DateField(
        required=True,
        label="Date",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date", "size": 10})
    )

    start_time = forms.TimeField(
        required=True,
        label="Début",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time", "step": "600", "size": 6})
    )

    end_time = forms.TimeField(
        required=True,
        label="Fin",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time", "step": "600", "size": 6})
    )

    message = forms.CharField(
        required=True,
        label="Message",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"})
    )

    class Meta:
        model = Appointment
        fields = ["date", "start_time", "end_time", "message"]


class EditAvailabilityForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(
        disabled=True,
        required=True,
        label="Jour",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.Select(attrs={"class": "form-select mx-2"})
    )

    start_time = forms.TimeField(
        required=False,
        label="Début",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TimeInput(attrs={"class": "form-control mx-2", "type": "time", "size": 6})
    )

    end_time = forms.TimeField(
        required=False,
        label="Fin",
        error_messages={"required": "Ce champs est obligatoire"},
        widget=forms.TimeInput(attrs={"class": "form-control mx-2", "type": "time", "size": 6})
    )

    class Meta:
        model = Availability
        fields = ["day_of_week", "start_time", "end_time"]


class BaseAvailabilityFormSet(BaseModelFormSet):
    def __init__(self, calendar_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Availability.objects.filter(calendar=calendar_id)

EditAvailabilityFormSet = modelformset_factory(
    Availability,
    formset=BaseAvailabilityFormSet,
    # form=EditAvailabilityForm,
    fields=["day_of_week", "start_time", "end_time"],
    max_num=7,
    labels={
        "day_of_week": False,
        "start_time": False,
        "end_time": False,
    },
    widgets={
        "day_of_week": forms.Select(attrs={"class": "form-select", "disabled": "disabled"}),
        "start_time": forms.TimeInput(attrs={"class": "form-control", "step": "600", "type": "time", "size": 6}),
        "end_time": forms.TimeInput(attrs={"class": "form-control", "step": "600", "type": "time", "size": 6}),
    },
)


class ServiceProviderFilterForm(forms.Form):
    search = forms.CharField(
        label="Recherche",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control me-2 w-10", "placeholder": "Rechercher"})
    )

    DAYS_OF_WEEK = Availability.DAYS_OF_WEEK.copy()
    DAYS_OF_WEEK.insert(0, ("", "-------"))
    day_of_week = forms.ChoiceField(
        choices=DAYS_OF_WEEK,
        label="Jour",
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 130px"})
    )

    start_time = forms.TimeField(
        label="Début",
        required=False,
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time", "style": "width: 80px"})
    )

    end_time = forms.TimeField(
        label="Fin",
        required=False,
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time", "style": "width: 80px"})
    )

    TOWNS = ServiceProvider.TOWNS.copy()
    TOWNS.insert(0, ("", "-------"))
    town = forms.ChoiceField(
        choices=TOWNS,
        label="Ville",
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 160px"})
    )

    LEVEL_OF_EDUCATION = ServiceProvider.LEVEL_OF_EDUCATION.copy()
    LEVEL_OF_EDUCATION.insert(0, ("", "-------"))
    level_of_education = forms.ChoiceField(
        choices=LEVEL_OF_EDUCATION,
        label="Education",
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 100px"})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Categorie",
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "style": "width: 120px"})
    )
