
from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.db.models import Q

from base_app.models import (
    Vehicles,
    RenterRegisterRequests,
)


class HomeView(View):
    def get(self, request: HttpRequest):
        context = {}

        # Search feature
        search_query = request.GET.get("search_query", "")
        query = (Q(vehicle_name__icontains=search_query) | Q(vehicle_desc__icontains=search_query)) & Q(is_available=True) & Q(can_be_listed=True)

        # Retrieve all objects which are approved to be listed(can_be_listed=True)
        context['vehicles'] = Vehicles.objects.filter(query)

        if request.user.is_authenticated and not request.user.is_renter:
            register_requests = RenterRegisterRequests.objects.filter(
                application_user=request.user, is_reviewed=False
            )

            # If a request already exists then notify the program
            # that the request already exists
            if register_requests.exists():
                context["is_already_requested"] = True

        return render(request, "base_app/home.html", context)
