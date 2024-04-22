
from django.http import HttpRequest
from django.shortcuts import reverse, redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages

from base_app.models import Review
from base_app.mixins import CustomLoginRequiredMixin


class OrderReviewEditView(CustomLoginRequiredMixin, View):
    def get(self, request: HttpRequest, review_id: str):
        review_queryset = Review.objects.filter(reference_id=review_id)
        if not review_queryset.exists():
            messages.warning(request, "You haven't reviewed this product yet.")
            return redirect(reverse("user_profile"))
        review = review_queryset.first()

        if review.data_generated_by != request.user:
            messages.error(request, "You are not allowed to edit this review")
            return redirect(reverse("user_profile_my_reviews"))

        return render(request, "base_app/dashboards/user_profile_order_review_edit.html", {
            "review": review
        })

    def post(self, request: HttpRequest, review_id: str):
        rating = int(request.POST.get("star"))
        description = request.POST.get("description", None)

        review: Review = get_object_or_404(Review, reference_id=review_id)
        if description is None:
            review.is_rating_only = True
        else:
            review.is_rating_only = False
            review.description = description
        review.rating = rating
        review.save()

        return redirect(reverse("user_profile_my_reviews"))
