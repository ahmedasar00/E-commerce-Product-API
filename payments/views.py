from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from orders.models import Order
from .models import Payment
# Assuming you have a form, if not, we can remove it.
# from .forms import PaymentForm


@login_required
def create_payment(request, order_id):
    """
    View to handle the payment process for a specific order.
    """
    # 1. Fetch the specific order for the logged-in user, or return a 404 error if not found.
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prevent re-payment for an already paid or non-pending order
    if order.status != "Pending Payment":
        # You can redirect to the order detail page with a message
        return redirect("order_detail", pk=order.id)

    if request.method == "POST":
        # This is where you would integrate a real payment gateway (e.g., Stripe, PayPal).
        # For this example, we will simulate a successful payment.

        # 2. Create a new Payment record and link it to the order.
        Payment.objects.create(
            order=order,
            amount=order.total_amount,
            status="Completed",
            transaction_id="dummy_transaction_12345",  # This would come from the payment gateway
        )

        # 3. Update the order's status to 'Processing' or 'Completed'.
        order.status = "Processing"
        order.save()

        # 4. Redirect the user to the order detail page to show the confirmation.
        return redirect("order_detail", pk=order.id)

    # If it's a GET request, just display the payment page with the order info.
    context = {"order": order}
    return render(request, "payments/create_payment.html", context)
