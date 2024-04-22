from django.http import HttpRequest
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages

from base_app.models import VehicleRent, Review, Notifications, NotificationType
from base_app.mixins import AuthRequiredMixin


class VehicleReviewCreateView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest, vehicle_rent_id: str):
        vehicle_rent: VehicleRent = get_object_or_404(VehicleRent, reference_id=vehicle_rent_id)
        if Review.objects.filter(vehicle=vehicle_rent.rent_request.vehicle, reviewer=request.user).exists():
            messages.warning(request, "You have already reviewed this renter!")
            return redirect(reverse("home"))

        return render(request, "base_app/reviews/user_profile_review_create.html", {
            "vehicle_rent": vehicle_rent
        })

    def post(self, request: HttpRequest, vehicle_rent_id: str):
        vehicle_rent: VehicleRent = get_object_or_404(VehicleRent, reference_id=vehicle_rent_id)
        rating = int(request.POST.get("star", 0))
        description = request.POST.get("description")

        if Review.objects.filter(vehicle=vehicle_rent.rent_request.vehicle, reviewer=request.user).exists():
            messages.warning(request, "You have already reviewed this renter!")
            return redirect(reverse("home"))

        if rating == 0:
            messages.error(request, "The rating cannot be null")
            return redirect(reverse("vehicle_review_create", args=[vehicle_rent_id]))

        Review(
            reviewer=request.user,
            description=' '.join(description.split()) or None,
            vehicle=vehicle_rent.rent_request.vehicle,
            rating=rating
        ).save()

        Notifications(
            notification_for=vehicle_rent.rent_request.vehicle.owner.application_user,
            message=f"You have been reviewd by {request.user.username} for vehicle {vehicle_rent.rent_request.vehicle.vehicle_name} for a rating of {rating}"
        ).save()

        return redirect(reverse("home"))
