from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest

from base_app.models import ApplicationUser, RenterRegisterRequests


def home_view(request: HttpRequest):
    context = {}
    
    register_requests = RenterRegisterRequests.objects.filter(
        application_user = request.user,
        is_reviewed = False
    )

    # If a request already exists then notify the program
    # that the request already exists
    if register_requests.exists() == True :
        context['is_already_requested'] = True

    return render(request, "base_app/home.html", context)

def handle_create_renter_register_request(request: HttpRequest):
    """
        EXTRACT renter_register_request user=current user, is_reviewed=False
        CHECK if requests already exists
        IF IT DOES:
            REDIRECT to home
        ELSE : 
            CREATE requests
    """
    register_requests = RenterRegisterRequests.objects.filter(
        application_user = request.user,
        is_reviewed = False
    )

    if register_requests.exists() == False :
        RenterRegisterRequests(application_user = request.user).save()
    
    return redirect(reverse('home'))

def admin_renter_register_requests_list_view(request: HttpRequest):
    register_requests = RenterRegisterRequests.objects.filter(is_reviewed=False)
    return render(
        request,
        "base_app/admin_renter_register_requests.html",
        {"requests": register_requests},
    )

def login_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "base_app/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            print("Logged in")

            return redirect(reverse("home"))

    """
        GET / Show Login
        POST /
        USERNAME, PASSWORD
        authenticate ->  User or None
        User check ( if user: )
        Login
    """


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home"))

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_no = request.POST["phone_no"]
        password = request.POST["password"]

        ApplicationUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_no=phone_no,
            password=password,
        ).save()
        return redirect(reverse("login"))

    return render(request, "base_app/register.html")

    """
        GET / Show Login Done
        POST / Done
        Extraction Done
        Create Done
        redirect to Login Done
    """


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse("home"))