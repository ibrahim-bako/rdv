from django.shortcuts import render, redirect
from django.contrib.auth import login as dj_login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import User, ServiceProvider
from appointment.models import Calendar, Availability

from .forms import RegisterForm, EditServiceProviderForm

def login(request):

    context = {"errors": []}

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if not user:
            context["errors"].append("Cet utilisateur n'existe pas.")

        user = authenticate(request=request, username=username, password=password)

        if not user:
            context["errors"].append("Vos identifiant sont incorect")
        else:
            dj_login(request=request, user=user)

    return render(request=request, template_name="account/login.html", context=context)


def register(request):

    context = {"errors": []}

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        register_form = RegisterForm(data=request.POST, files=request.FILES)
        context["register_form"] = register_form

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        is_service_provider = request.POST.get("is_service_provider")
        avatar = request.FILES.get("avatar")

        if not (username or password or confirm_password or first_name or last_name or email or phone_number):
            context["errors"].append("Tous les champ sont obligatoir")
            return render(request=request, template_name="account/register.html", context=context)

        user = User.objects.filter(username=username).first()
        if user is not None:
            context["errors"].append("Cet utilisateur existe déjà")
            return render(request=request, template_name="account/register.html", context=context)

        if not password == confirm_password:
            context["errors"].append("Les mots de passe ne corresponde pas")
            return render(request=request, template_name="account/register.html", context=context)


        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            avatar=avatar,
        )

        user.set_password(password)
        user.save()

        dj_login(request=request, user=user)

        if is_service_provider:
            return redirect("become_service_provider")

    context["register_form"] = RegisterForm()

    return render(request=request, template_name="account/register.html", context=context)

@login_required(login_url="login", redirect_field_name="become_service_provider")
def become_service_provider(request):
    context = {"errors": []}

    user = request.user

    service_provider = ServiceProvider.objects.filter(user=request.user).first()
    if service_provider:
        return redirect("home")

    if request.method == "POST":

        edit_service_provider_form = EditServiceProviderForm(data=request.POST)
        context["edit_service_provider_form"] = edit_service_provider_form

        if edit_service_provider_form.is_valid():
            service_provider = edit_service_provider_form.save(commit=False)
            service_provider.user = user
            service_provider.save()

            calendar = Calendar.objects.create(owner=service_provider)

            for day in Availability.DAYS_OF_WEEK:
                Availability.objects.create(day_of_week=day, calendar=calendar)

            return redirect("home")

    context["edit_service_provider_form"] = EditServiceProviderForm()

    return render(request=request, template_name="account/become_service_provider.html", context=context)
