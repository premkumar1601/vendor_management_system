# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, VendorPerformanceViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceViewSet.as_view({'get': 'retrieve'}), name='vendor_performance'),
    path('api/purchase_orders/<int:pk>/acknowledge/', PurchaseOrderViewSet.as_view({'post': 'acknowledge'}), name='acknowledge_purchase_order'),
]
