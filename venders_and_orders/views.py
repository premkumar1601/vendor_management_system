from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated  
from rest_framework.authentication import TokenAuthentication 
from django.utils import timezone
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  

    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()

        if purchase_order.acknowledgment_date:
            return Response({'message': 'Purchase order has already been acknowledged'}, status=status.HTTP_400_BAD_REQUEST)
    
        purchase_order.status = 'acknowledged'
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({'message': 'Purchase order acknowledged successfully'}, status=200)

class VendorPerformanceViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    
    def retrieve(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)
