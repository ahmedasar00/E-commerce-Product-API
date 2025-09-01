from rest_framework import viewsets, permissions, filters
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Review, Product  # Assuming Product model is accessible
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

# --- Django REST Framework API Views ---


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting reviews.

    Provides a full CRUD API for reviews.
    - Anyone can view reviews.
    - Only authenticated users can create reviews.
    - Only the author of a review can update or delete it.

    Filtering:
    - You can order reviews by rating using the `ordering` query parameter.
      Example: `/api/reviews/?ordering=-rating` to get highest rated first.
    """

    queryset = Review.objects.all().select_related("user", "product")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["rating", "created_at"]  # Fields available for ordering
    ordering = ["-created_at"]  # Default ordering

    def perform_create(self, serializer):
        """
        Automatically associate the current logged-in user with a new review.
        """
        serializer.save(user=self.request.user)


# --- Django Template-Based Views ---


class ReviewListView(ListView):
    """
    Displays a list of all reviews.
    """

    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        """
        Optionally filter reviews by a product if a 'product_id' is in the URL query.
        """
        queryset = super().get_queryset().select_related("user", "product")
        product_id = self.request.GET.get("product_id")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Allows a logged-in user to create a new review.
    """

    model = Review
    fields = ["product", "rating", "comment"]
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("review-list")

    def form_valid(self, form):
        """
        Assign the current logged-in user as the author of the review.
        """
        form.instance.user = self.request.user
        # You might want to add a check here to prevent duplicate reviews
        # before calling super().form_valid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add form title to context.
        """
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add a New Review"
        # Pass a list of products to the template for the dropdown
        context["products"] = Product.objects.all()
        return context


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the author of a review to update it.
    """

    model = Review
    fields = ["rating", "comment"]
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("review-list")

    def test_func(self):
        """
        Check if the current user is the author of the review.
        """
        review = self.get_object()
        return self.request.user == review.user

    def get_context_data(self, **kwargs):
        """
        Add form title to context.
        """
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Your Review"
        return context


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the author of a review to delete it after confirmation.
    """

    model = Review
    template_name = "reviews/review_confirm_delete.html"
    success_url = reverse_lazy("review-list")

    def test_func(self):
        """
        Check if the current user is the author of the review.
        """
        review = self.get_object()
        return self.request.user == review.user
