from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline representation of OrderItem model for the Order admin view.
    Allows adding and editing OrderItems directly within the Order view.
    """

    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Order model.
    Displays key order information and includes an inline for OrderItems.
    """

    inlines = [OrderItemInline]
    list_display = ("id", "user", "address", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
