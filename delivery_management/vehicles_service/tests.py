from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Component, Vehicle, VehicleIssue

class VehicleServiceTests(APITestCase):

    def setUp(self):
        # Create a component for testing
        self.component = Component.objects.create(
            name='Brake Pad',
            price=50.00,
            repair_price=25.00,
            is_new=True
        )

        # Create a vehicle for testing
        self.vehicle = Vehicle.objects.create(
            name='Toyota',
            model='Corolla'
        )

    def test_add_component(self):
        url = reverse('add-component')
        data = {
            'name': 'Oil Filter',
            'price': 20.00,
            'repair_price': 10.00,
            'is_new': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Component.objects.count(), 2)  # 1 existing + 1 new

    def test_add_component_missing_field(self):
        url = reverse('add-component')
        data = {
            'name': 'Air Filter',
            'price': 15.00,
            'repair_price': 5.00
            # 'is_new' is missing
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Error', response.data)

    def test_get_service_cost(self):
        url = reverse('get-service-cost')
        data = {
            'vehicle_name': 'Toyota',
            'model_no': 'Corolla',
            'part_name': 'Brake Pad',
            'is_repair': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], self.component.price)

    def test_get_service_cost_invalid_part(self):
        url = reverse('get-service-cost')
        data = {
            'vehicle_name': 'Toyota',
            'model_no': 'Corolla',
            'part_name': 'Invalid Part',
            'is_repair': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Error', response.data)

    def test_add_vehicle_for_service(self):
        url = reverse('add-vehicle-for-service')
        data = {
            'name': 'Toyota',
            'model': 'Corolla',
            'part_name': 'Brake Pad',
            'is_repair': False,
            'register': 'ABC123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(VehicleIssue.objects.count(), 1)

    def test_add_vehicle_for_service_missing_field(self):
        url = reverse('add-vehicle-for-service')
        data = {
            'name': 'Toyota',
            'model': 'Corolla',
            # Missing part_name
            'is_repair': False,
            'register': 'ABC123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Error', response.data)

# Create your tests here.
