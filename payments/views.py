from django.shortcuts import render

# Create your views here.
# payments/views.py

from django.shortcuts import render, redirect
from .forms import PaymentForm


def create_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PaymentForm()

    return render(request, "payments/create_payment.html", {"form": form})
