from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='admin', password='admin@123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_vendor_endpoints(self):
        # Create a vendor
        response = self.client.post('/api/vendors/', {'name': 'Vendor 1', 'contact_details': 'Contact', 'address': 'Address', 'vendor_code': '123'})
        self.assertEqual(response.status_code, 201)

        # Retrieve all vendors
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Retrieve a specific vendor
        vendor_id = response.data[0]['id']
        response = self.client.get(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, 200)

        # Update a vendor
        response = self.client.put(f'/api/vendors/{vendor_id}/', {'name': 'Vendor 1', 'contact_details': 'Updated Contact details', 'address': 'Address2', 'vendor_code': '123'})
        self.assertEqual(response.status_code, 200)

        # Update a patch - quality_rating_avg is a computed key and cannot be updated by api
        response = self.client.put(f'/api/vendors/{vendor_id}/', {'quality_rating_avg' : 1})
        self.assertEqual(response.status_code, 400)

        # Delete a vendor
        response = self.client.delete(f'/api/vendors/{vendor_id}/')
        self.assertEqual(response.status_code, 204)

    def test_purchase_order_endpoints(self):
        # Create a vendor for testing purchase orders
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='Contact', address='Address', vendor_code='123')

        # Create a purchase order
        response = self.client.post('/api/purchase_orders/', {'po_number': 'PO-001', 'vendor': vendor.id, 'order_date': '2024-05-05T10:00:00Z', 'delivery_date': '2024-05-10T10:00:00Z', 'items': '[{"Product Name" : "P1", "price" : "40"}]', 'quantity': 10, 'status': 'pending'})
        self.assertEqual(response.status_code, 201)

        # Retrieve all purchase orders
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Retrieve a specific purchase order
        po_id = response.data[0]['id']
        response = self.client.get(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, 200)

        # Update a purchase order - Try to set status complete while still the vender has not yet acknowledged the order
        response = self.client.patch(f'/api/purchase_orders/{po_id}/', {'status': 'completed'})
        self.assertEqual(response.status_code, 400)

        # Acknowledge a purchase order
        response = self.client.post(f'/api/purchase_orders/{po_id}/acknowledge/')
        self.assertEqual(response.status_code, 200)

        # Update a status of order
        response = self.client.patch(f'/api/purchase_orders/{po_id}/', {'status': 'completed'})
        self.assertEqual(response.status_code, 200)

        # Delete a purchase order
        response = self.client.delete(f'/api/purchase_orders/{po_id}/')
        self.assertEqual(response.status_code, 204)
