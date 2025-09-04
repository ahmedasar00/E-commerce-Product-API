from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Address
from .forms import AddressForm


def register_view(request):
    """
    Handle user registration.
    - If POST: validate and create user, then log them in.
    - If GET: show registration form.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the new user
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    """
    Handle user login.
    - If POST: authenticate and log in the user.
    - If GET: show login form.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def profile_view(request):
    """
    Show user profile page.
    Only accessible when logged in.
    """
    return render(request, "users/profile.html")


def logout_view(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    return redirect("login")


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = "users/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        """
        Ensure users can only see their own addresses.
        """
        return Address.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "users/address_form.html"
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        """
        Assign the current user to the new address before saving.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "users/address_form.html"
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        """
        Ensure users can only edit their own addresses.
        """
        return Address.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = "users/address_confirm_delete.html"
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        """
        Ensure users can only delete their own addresses.
        """
        return Address.objects.filter(user=self.request.user)


# --- Static Pages (simple render only) ---


def home(request):
    """Render home page."""
    return render(request, "home.html")


def about(request):
    """Render about page."""
    return render(request, "about.html")


def contact(request):
    """Render contact page."""
    return render(request, "contact.html")


def services(request):
    """Render services page."""
    return render(request, "services.html")


def products(request):
    """Render products listing page."""
    return render(request, "products.html")


def product_details(request):
    """Render details page for a product (static example)."""
    return render(request, "product_details.html")
