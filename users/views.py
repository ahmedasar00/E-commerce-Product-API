from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json  # 👈 Import the json library


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        # Check if the request body is JSON
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

            # Pass the parsed JSON data to the form
            form = CustomUserCreationForm(data)
        else:
            # Handle standard form data
            form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # login(request, user) # You might not need to log in the user for an API call
            return JsonResponse(
                {"message": "User registered successfully!"}, status=201
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # ... rest of your view for GET requests
    return render(request, "users/register.html", {"form": form})


# Add the decorator to disable CSRF protection
@csrf_exempt
def login_view(request):
    """
    Handles user login. Returns a JSON response for API requests.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Return a success message in JSON format for the API client
                return JsonResponse(
                    {"message": "Login successful!", "username": user.username}
                )
            else:
                # Handle invalid credentials
                return JsonResponse(
                    {"message": "Invalid username or password."}, status=401
                )
        else:
            # Return form errors in JSON format
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        # For a GET request, render the HTML form
        form = AuthenticationForm()
        return render(request, "users/login.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "users/profile.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def services(request):
    return render(request, "services.html")


def products(request):
    return render(request, "products.html")


def product_details(request):
    return render(request, "product_details.html")
