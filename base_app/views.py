from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.http import HttpRequest
from django.contrib import messages
from django.views import View

from base_app.models import (
    ApplicationUser,
    AdminUser,
    RenterUser,
    RenterRegisterRequests,
    RenterRegisterResults,
    Vehicles,
    VehicleListingRequests,
    Notifications
)
from base_app.mixins import AuthRequiredMixin, AdminRequiredMixin


class HomeView(View):
    def get(self, request: HttpRequest):
        context = {}

        # Retrieve all objects which are approved to be listed(can_be_listed=True)
        context['vehicles'] = Vehicles.objects.filter(can_be_listed=True,
                                                      is_available=True)

        if request.user.is_authenticated and not request.user.is_renter:
            register_requests = RenterRegisterRequests.objects.filter(
                application_user=request.user, is_reviewed=False
            )

            # If a request already exists then notify the program
            # that the request already exists
            if register_requests.exists():
                context["is_already_requested"] = True

        return render(request, "base_app/home.html", context)


class HandleCreateRenterRegisterRequest(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Filter RenterRegisterRequests with the condition such that:
        # 1. The user who made the request( application_user ) is the current user ( request.user )
        # 2. The request is pending i.e is_reviewed = False
        register_requests = RenterRegisterRequests.objects.filter(
            application_user=request.user, is_reviewed=False
        )

        # OPTIMAL CASE: register_requests.exists() should be False because in optimal cases no previous requests
        # should have been made

        # SUB-OPTIMAL CASE: register_requests.exists() becomes True and there is 1 item i.e RenterRegisterRequests
        # In this case, this indicates that the requests has already been made before and is yet
        # to be reviewed by the admin

        # ERROR CASE: register_requests.exists() becomes True and there is >1 item.

        # QuerySet<[]> = False
        # QuerySet<[RenterRegisterRequests, ...]> = True
        if register_requests.exists() is False:
            # Create a new request to register as a renter
            RenterRegisterRequests(application_user=request.user).save()

        return redirect(reverse("home"))


class HandleRejectRegisterRequest(View):
    def post(self, request: HttpRequest):
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed in RenterRegisterRequest to True ✅
        CREATE new RenterRegisterResult and set the is_approved to False ✅
        """
        request_id = request.POST["request_id"]
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)
        register_request.is_reviewed = True

        # Get ApplicationUser from request.user and get its
        # corresponding AdminUser object
        current_admin_user = AdminUser.objects.get(application_user=request.user)

        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=False,  # Because the request was rejected
        ).save()
        register_request.save()

        return redirect(reverse("admin_renter_register_list"))


class HandleAcceptRegisterRequest(AuthRequiredMixin, View):
    def post(self, request: HttpRequest):
        """
        EXTRACT request_id from POST request ✅
        GET RenterRegisterRequests object using that request_id ✅
        CHANGE is_reviewed to TRUE ✅
        CHANGE that user's is_renter value to True ✅
        RETRIEVE the current admin user ✅
        CREATE RenterRequest result and set is_approved to True ✅
        """

        # EXTRACT values from the POST request
        # {
        # "csrfmiddlewaretoken": "~~~~~",
        # "request_id": "~~~~~"  <-- We need this
        # }
        request_id = request.POST["request_id"]

        # Because we are filtering using the PRIMARY KEY i.e request_id
        # we can be sure that only one associated request ( RenterRegisterRequests ) can exist
        # That's why we are using .get() instead of .filter()
        register_request = RenterRegisterRequests.objects.get(reference_id=request_id)

        # Setting the is_reviewed field of the request to True
        register_request.is_reviewed = True

        ################################################################################################
        # current_application_user: ApplicationUser = request.user
        # HOW WAS IT FIXED: here's request.user returns the current user i.e admin
        # However, the value is_renter field to be changed is the ApplicationUser's not admin's
        # Hence, we use the value of register_request.application_user which gives back the user making the request
        requester: ApplicationUser = (
            register_request.application_user
        )  # The one who requested i.e Client not Admin
        requester.is_renter = True
        requester.save()

        # Using the current logged in user ( request.user ) which is an ApplicationUser
        # and filtering the corresponding AdminUser using the FK application_user
        # by comparing it with current ( ApplicationUser ) user.
        current_admin_user = AdminUser.objects.get(application_user=request.user)

        # Created a new Result
        RenterRegisterResults(
            renter_request=register_request,
            reviewed_by=current_admin_user,
            is_approved=True,  # Because we have accepted
        ).save()
        register_request.save()

        # Create a RenterUser
        RenterUser(
            application_user=requester  # Create a corresponding RenterUser for the requester
        ).save()

        return redirect(reverse("admin_renter_register_list"))


class AdminRenterRegisterRequestsListView(AuthRequiredMixin, AdminRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Filter Renter Register Requests on the basis of the condition that the
        # request is pending i.e is_reviewed = False
        register_requests = RenterRegisterRequests.objects.filter(is_reviewed=False)

        return render(
            request,  # REQUEST
            "base_app/admin_renter_register_requests.html",  # TEMPLATE
            {"requests": register_requests},  # CONTEXT
        )

        return redirect(reverse("home"))


class AdminVehicleListingRequestsListView(AuthRequiredMixin, AdminRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Filter Renter Register Requests on the basis of the condition that the
        # request is pending i.e is_reviewed = False
        vehicle_listing_request = VehicleListingRequests.objects.filter(
            is_reviewed=False
        )

        return render(
            request,  # REQUEST
            "base_app/admin_vehicle_listing_request.html",  # TEMPLATE
            {"requests": vehicle_listing_request},  # CONTEXT
        )

        return redirect(reverse("home"))


class HandleRejectVehicleListingRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest, request_id: str):
        vehicle_request = VehicleListingRequests.objects.get(reference_id=request_id)
        vehicle_request.vehicle.delete()

        return redirect(reverse("admin_vehicle_listing_request_list"))


class HandleAcceptVehicleListingRequest(AuthRequiredMixin, AdminRequiredMixin, View):
    def post(self, request: HttpRequest, request_id: str):
        vehicle_request = VehicleListingRequests.objects.get(reference_id=request_id)

        vehicle = vehicle_request.vehicle
        vehicle_request.is_reviewed = True
        vehicle.can_be_listed = True

        vehicle.save()
        vehicle_request.save()

        return redirect(reverse("admin_vehicle_listing_request_list"))


class VehicleAddForListingView(AuthRequiredMixin, View):
    def post(self, request: HttpRequest):
        name = request.POST["vehicle_name"]
        desc = request.POST["vehicle_desc"]
        company = request.POST["vehicle_company"]
        vtype = request.POST["vehicle_type"]
        seater = request.POST["vehicle_seater"]
        number_plate = request.POST["vehicle_number_plate"]

        docs = request.FILES.get("vehicle_documents")
        desc_img = request.FILES.get("vehicle_description_image")

        current_renter_user = RenterUser.objects.get(application_user=request.user)

        this_vehicle = Vehicles(
            owner=current_renter_user,
            vehicle_name=name,
            vehicle_desc=desc,
            vehicle_company=company,
            vehicle_type=vtype,
            vehicle_seater=seater,
            vehicle_number_plate=number_plate,
            vehicle_documents=docs,
            vehicle_description_image=desc_img,
        )
        this_vehicle.save()

        VehicleListingRequests(
            vehicle=this_vehicle,
        ).save()

        return render(request, "base_app/vehicle_add_for_listing.html")


class NotificationListView(AuthRequiredMixin, View):
    redirect_if_not_authed = reverse_lazy("home")

    def get(self, request: HttpRequest, request_id: str, code=3):
        notification_queryset = Notifications.objects.filter(notification_for=request.user)

        # Flag all unread notifications(is_read=False) to read(is_read=True)
        for nf in notification_queryset.filter(is_read=False):
            nf.is_read = True
            nf.save()

        return render(request, "base_app/notification_list.html", {
            "notifications": notification_queryset,
        })


class LoginView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "base_app/login.html")

    def post(self, request: HttpRequest):
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            # Alert that the user is logged in
            login(request, user)
            messages.success(request, "You have logged in successfully")
            return redirect(reverse("home"))

        messages.error(request, "The user details has gone wrong!")
        return redirect(reverse("login"))


class RegisterView(AuthRequiredMixin, View):
    """
        GET / Show Login Done
        POST / Done
        Extraction Done
        Create Done
        redirect to Login Done
    """

    def get(self, request: HttpRequest):
        return render(request, "base_app/register.html")

    def post(self, request: HttpRequest):
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


class HandleLogout(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            messages.success(request, "Logged out Successfully!")
            logout(request)
        return redirect(reverse("home"))
