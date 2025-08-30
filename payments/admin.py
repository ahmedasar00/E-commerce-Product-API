from django.contrib import admin
from .models import Payment


# Register your models here.
@admin.register(Payment)
class paymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "amount",
        "payment_method",
        "transaction_id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "payment_method")
    search_fields = ("order__id", "transaction_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
