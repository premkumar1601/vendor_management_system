from django.db import models
from django.db.models.signals import post_save
from django.db.models import Avg, ExpressionWrapper, fields, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    quality_rating = models.FloatField(null=True, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    issue_date = models.DateTimeField(default=timezone.now, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        # Calculate on-time delivery rate
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_pos = completed_pos.filter(delivery_date__lte=instance.delivery_date)
        on_time_delivery_rate = on_time_pos.count() / completed_pos.count()
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

        # Calculate quality rating average
        completed_pos_with_rating = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

        # Calculate fulfillment rate
        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        successful_pos = total_pos.filter(status='completed')
        fulfillment_rate = successful_pos.count() / total_pos.count()
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def calculate_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        vendor = instance.vendor
        response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).exclude(issue_date__isnull=True)
        if response_times.exists():
            avg_response_time = response_times.aggregate(avg_response=Avg(ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())))['avg_response']
            if avg_response_time:
                avg_response_time_seconds = avg_response_time.total_seconds()
                vendor.average_response_time = avg_response_time_seconds
                vendor.save()


