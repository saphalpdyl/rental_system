from django.shortcuts import render
from django.views import View
from django.http import HttpRequest

from base_app.models import Review, Ratings

from base_app.mixins import AuthRequiredMixin


class UserProfileMyReviewsView(AuthRequiredMixin, View):
    def get(self, request: HttpRequest):
        reviews = Review.objects.filter(reviewer=request.user)

        if request.user.is_renter:
            reviews = Review.objects.filter(vehicle__owner__application_user=request.user)

        return render(request, "base_app/reviews/user_profile_my_reviews.html", {
            "reviews": reviews,
            "ratings": Ratings
        })