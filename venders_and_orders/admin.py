from django.contrib import admin
from .models import Vendor, PurchaseOrder


class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    readonly_fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate', 'created_at', 'updated_at')

class PurchaseOrdersAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'vendor', 'issue_date', 'acknowledgment_date', 'status']
    readonly_fields = ('order_date', 'created_at', 'updated_at')
    list_filter = ('vendor', 'status')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrdersAdmin)
