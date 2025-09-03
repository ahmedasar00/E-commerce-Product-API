from django.shortcuts import render


def home_view(request):
    """
    This view is responsible for rendering the home page.
    """
    return render(request, "home.html")
