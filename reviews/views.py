from django.views.generic import ListView, DetailView
from reviews.models import Review


class ReviewListView(ListView):
    """
    A view to display a list of all reviews.
    """

    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"


class ReviewDetailView(DetailView):
    """
    A view to display the details of a single review.
    """

    model = Review
    template_name = "reviews/review_detail.html"
    context_object_name = "review"
