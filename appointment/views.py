from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import EditAvailabilityFormSet, CreateAppointmentForm, ServiceProviderFilterForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.core.mail import send_mail

from django.utils.dateparse import parse_time

from .models import Calendar, Appointment, Availability

from account.models import ServiceProvider
from account.forms import EditServiceProviderForm

User = get_user_model()


def search_service_provider(request):

    context = {}

    service_providers = ServiceProvider.objects.all()

    if request.method == "POST":

        service_provider_filter_form = ServiceProviderFilterForm(data=request.POST)
        context["form"] = service_provider_filter_form

        if service_provider_filter_form.is_valid():

            category = service_provider_filter_form.cleaned_data["category"]
            town = service_provider_filter_form.cleaned_data["town"]
            level_of_education = service_provider_filter_form.cleaned_data["level_of_education"]
            day_of_week = service_provider_filter_form.cleaned_data["day_of_week"]
            search = service_provider_filter_form.cleaned_data["search"]
            start_time = service_provider_filter_form.cleaned_data["start_time"]
            end_time = service_provider_filter_form.cleaned_data["end_time"]

            if category :
                service_providers = service_providers.filter(category__value=category)

            if day_of_week:
                service_providers = service_providers.filter(
                    Q(calendar__availabilities__day_of_week=day_of_week) and
                    Q(calendar__availabilities__start_time__isnull=False) and
                    Q(calendar__availabilities__end_time__isnull=False)
                )

            if start_time :
                service_providers = service_providers.filter(calendar__availabilities__start_time__lte=start_time)
            if end_time :
                service_providers = service_providers.filter(calendar__availabilities__end_time__gte=end_time)

            if level_of_education:
                service_providers = service_providers.filter(level_of_education=level_of_education)

            if search :
                service_providers = service_providers.filter(
                    Q(description__icontains=search) |
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(town__icontains=search) |
                    Q(work__icontains=search)
                )

            if town:
                service_providers = service_providers.filter(town=town)
    else:
        service_provider_filter_form = ServiceProviderFilterForm()
        context["form"] = service_provider_filter_form

    context["service_providers"] = service_providers.distinct()

    return render(request=request, template_name="appointment/search_service_provider.html", context=context)

def service_provider_detail(request, service_provider_id):
    context = {}

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        appointment = CreateAppointmentForm(request.POST)

        if appointment.is_valid():
            service_provider = ServiceProvider.objects.get(pk=service_provider_id)
            owner = User.objects.get(pk=service_provider.user.pk)
            calendar = Calendar.objects.get(owner=service_provider.pk)
            availabilities = Availability.objects.filter(calendar=calendar)

            appointment = appointment.save(commit=False)

            appointment.attende = request.user
            appointment.calendar = calendar

            appointment.save()

            send_mail(
                subject="Demande de rendez-vous",
                message=service_provider_appointment_request(service_provider=service_provider, user=request.user, appointment=appointment),
                html_message=service_provider_appointment_request(service_provider=service_provider, user=request.user, appointment=appointment),
                from_email= "rdv.uvbf@gmail.com",
                recipient_list=[service_provider.email],
                fail_silently=False,
            )

            send_mail(
                subject="Demande de rendez-vous",
                message=user_appointment_request(service_provider=service_provider, user=request.user, appointment=appointment),
                html_message=user_appointment_request(service_provider=service_provider, user=request.user, appointment=appointment),
                from_email= "rdv.uvbf@gmail.com",
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            return redirect("home")

    appointment_form = CreateAppointmentForm()
    context["appointment_form"] = appointment_form

    service_provider = ServiceProvider.objects.get(pk=service_provider_id)
    owner = User.objects.get(pk=service_provider.user.pk)
    calendar = Calendar.objects.get(owner=service_provider.pk)
    availabilities = Availability.objects.filter(calendar=calendar)

    context["owner"] = owner
    context["service_provider"] = service_provider
    context["calendar"] = calendar
    context["availabilities"] = availabilities

    return render(request=request, template_name="appointment/service_provider_detail.html", context=context)

@login_required(login_url="login", redirect_field_name="my_appointments")
def my_appointments(request):

    context = {}

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if not service_provider:
        return redirect("create_service_provider")

    pending_appointments = Appointment.objects.filter(status="PENDING", calendar__owner=service_provider.pk)
    accepted_appointments = Appointment.objects.filter(status="ACCEPTED", calendar__owner=service_provider.pk)

    context["pending_appointments"] = pending_appointments
    context["accepted_appointments"] = accepted_appointments

    return render(request=request, template_name="appointment/my_appointments.html", context=context)

@login_required(login_url="login", redirect_field_name="my_appointments")
def accept_appointment(request, appointment_id):

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if not service_provider:
        return redirect("create_service_provider")

    pending_appointments = Appointment.objects.get(pk=appointment_id, calendar__owner=service_provider)
    pending_appointments.status = "ACCEPTED"
    pending_appointments.save()

    send_mail(
        subject="Demande de rendez-vous accepter",
        message=user_appointment_accepted(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        html_message=user_appointment_accepted(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        from_email= "rdv.uvbf@gmail.com",
        recipient_list=[pending_appointments.attende.email],
        fail_silently=False,
    )

    return redirect("my_appointments")

@login_required(login_url="login", redirect_field_name="my_appointments")
def cancel_appointment(request, appointment_id):

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if not service_provider:
        return redirect("create_service_provider")

    pending_appointments = Appointment.objects.get(pk=appointment_id)
    pending_appointments.status = "CANCELLED"
    pending_appointments.save()

    send_mail(
        subject="Demande de rendez-vous annuler",
        message=user_appointment_cancelled(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        html_message=user_appointment_cancelled(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        from_email= "rdv.uvbf@gmail.com",
        recipient_list=[pending_appointments.attende.email],
        fail_silently=False,
    )

    return redirect("my_appointments")

@login_required(login_url="login", redirect_field_name="my_appointments")
def reject_appointment(request, appointment_id):

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if not service_provider:
        return redirect("create_service_provider")

    pending_appointments = Appointment.objects.get(pk=appointment_id)
    pending_appointments.status = "REJECTED"
    pending_appointments.save()

    send_mail(
        subject="Demande de rendez-vous annuler",
        message=user_appointment_rejected(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        html_message=user_appointment_rejected(service_provider=service_provider, user=pending_appointments.attende, appointment=pending_appointments),
        from_email= "rdv.uvbf@gmail.com",
        recipient_list=[pending_appointments.attende.email],
        fail_silently=False,
    )

    return redirect("my_appointments")


@login_required(login_url="login", redirect_field_name="edit_calendar")
def edit_calendar(request):

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if not service_provider:
        return redirect("create_service_provider")

    context = {}

    if request.method == "POST":
        _service_provider = service_provider
        _calendar = Calendar.objects.get(owner=_service_provider.pk)

        edit_service_srovider_form = EditServiceProviderForm(data=request.POST, instance=_service_provider)

        if edit_service_srovider_form.is_valid():
            service_provider = edit_service_srovider_form.save(commit=False)
            service_provider.save()

        DAYS_OF_WEEK = [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ]

        for i in range(0, 7):
            day_of_week = DAYS_OF_WEEK[i]
            start_time = request.POST.get(f"form-{i}-start_time")
            end_time = request.POST.get(f"form-{i}-end_time")

            availability = Availability.objects.filter(calendar=_calendar.pk, day_of_week=day_of_week).first()
            availability.start_time = parse_time(start_time)
            availability.end_time = parse_time(end_time)
            availability.save()

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    calendar = Calendar.objects.filter(owner=service_provider.pk).first()

    edit_availability_formset = EditAvailabilityFormSet(calendar_id=calendar.pk)
    edit_service_srovider_form = EditServiceProviderForm(instance=service_provider)

    context["edit_availability_formset"] = edit_availability_formset
    context["edit_service_srovider_form"] = edit_service_srovider_form

    return render(request=request, template_name="appointment/edit_calendar.html", context=context)


def service_provider_appointment_request(service_provider, user, appointment):
    return f"""
    <body>
        <div>
            <h4>Bonjour, <strong>{service_provider.user}</strong></h4>
            <p>
                Vous venez de recevoir une demande de rendez-vous de <strong>{user}</strong> le <strong>{appointment.date} à {appointment.start_time}</strong>.
                <cite>
                    {appointment.message}
                </cite>
            </p>
        </div>
    </body>
"""

def user_appointment_request(service_provider, user, appointment):
    return f"""
    <body>
        <div>
            <h4>Bonjour, <strong>{user}</strong></h4>
            <p>
                Vous avez demandé un rendez-vous à <strong>{service_provider.user}</strong> pour le <strong>{appointment.date} à {appointment.start_time}</strong>.
            </p>
        </div>
    </body>
"""

def user_appointment_accepted(service_provider, user, appointment):

    return f"""
    <body>
        <div>
            <h4>Bonjour, <strong>{user}</strong></h4>
            <p>
                Votre demande de rendez-vous à <strong>{service_provider.user}</strong> pour le <strong>{appointment.date} à {appointment.start_time}</strong> a été <strong>accepter</strong>.
            </p>
        </div>
    </body>
"""

def user_appointment_cancelled(service_provider, user, appointment):

    return f"""
    <body>
        <div>
            <h4>Bonjour, <strong>{user}</strong></h4>
            <p>
                Votre demande de rendez-vous à <strong>{service_provider.user}</strong> pour le <strong>{appointment.date} à {appointment.start_time}</strong> a été <strong>annuler</strong>.
            </p>
        </div>
    </body>
"""

def user_appointment_rejected(service_provider, user, appointment):

    return f"""
    <body>
        <div>
            <h4>Bonjour, <strong>{user}</strong></h4>
            <p>
                Votre demande de rendez-vous à <strong>{service_provider.user}</strong> pour le <strong>{appointment.date} à {appointment.start_time}</strong> a été <strong>rejeter</strong>.
            </p>
        </div>
    </body>
"""
