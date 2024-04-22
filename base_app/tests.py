from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from base_app.models import *

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # Test user registration
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            # Add other required fields
        })
        self.assertEqual(response.status_code, 302) # Redirect to login page after successful registration
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_user_login(self):
        # Test user login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302) # Redirect to home page after successful login
        self.assertTrue('_auth_user_id' in self.client.session)

class VehicleListingTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.vehicle = Vehicles.objects.create(vehicle_name='Test Vehicle', price=100, can_be_listed=True, is_available=True)

    def test_vehicle_listing(self):
        # Test vehicle listing
        response = self.client.get(reverse('buyer_vehicle_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vehicle')

class TransactionRequestTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.vehicle = Vehicles.objects.create(vehicle_name='Test Vehicle', price=100, can_be_listed=True, is_available=True)
        self.vehicle_rent = VehicleRent.objects.create(rent_request=self.vehicle, status=VehicleRentStatus.ACTIVE)

    def test_transaction_request(self):
        # Test transaction request
        response = self.client.post(reverse('transaction_request_respond', args=[self.vehicle_rent.reference_id]), {
            # Add required fields for transaction request
        })
        self.assertEqual(response.status_code, 302) # Redirect to some page after successful transaction request
        self.assertTrue(TransactionRequest.objects.filter(renting_request=self.vehicle_rent).exists())

class NotificationManagementTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notification = Notifications.objects.create(notification_for=self.user, message='Test Notification', is_read=False)

    def test_notification_creation(self):
        # Test notification creation
        self.assertTrue(Notifications.objects.filter(message='Test Notification').exists())

    def test_notification_read(self):
        # Test marking notification as read
        response = self.client.post(reverse('notification_list_view'), {
            'notification_id': self.notification.reference_id,
        })
        self.assertEqual(response.status_code, 302) # Redirect to notification list view after marking as read
        notification = Notifications.objects.get(reference_id=self.notification.reference_id)
        self.assertTrue(notification.is_read)

class UserProfileUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_update(self):
        # Test user profile update
        response = self.client.post(reverse('user_profile_update'), {
            'first_name': 'Test',
            'last_name': 'User',
            # Add other profile fields
        })
        self.assertEqual(response.status_code, 302) # Redirect to profile page after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')

class VehicleCategoryListingTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.vehicle = Vehicles.objects.create(vehicle_name='Test Vehicle', price=100, can_be_listed=True, is_available=True, category='Sedan')

    def test_vehicle_category_listing(self):
        # Test vehicle listing by category
        response = self.client.get(reverse('vehicle_category_list', args=['Sedan']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vehicle')

class VehicleRentRequestTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.vehicle = Vehicles.objects.create(vehicle_name='Test Vehicle', price=100, can_be_listed=True, is_available=True)

    def test_vehicle_rent_request(self):
        # Test vehicle rent request
        response = self.client.post(reverse('vehicle_rent_request', args=[self.vehicle.id]), {
            'start_date': '2023-04-01',
            'end_date': '2023-04-10',
        })
        self.assertEqual(response.status_code, 302) # Redirect to some page after successful rent request
        self.assertTrue(VehicleRent.objects.filter(rent_request=self.vehicle).exists())

class TransactionRequestApprovalTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.vehicle = Vehicles.objects.create(vehicle_name='Test Vehicle', price=100, can_be_listed=True, is_available=True)
        self.vehicle_rent = VehicleRent.objects.create(rent_request=self.vehicle, status=VehicleRentStatus.ACTIVE)
        self.transaction_request = TransactionRequest.objects.create(renting_request=self.vehicle_rent, status=TransactionStatus.PENDING)

    def test_transaction_request_approval(self):
        # Test transaction request approval
        response = self.client.post(reverse('transaction_request_approve', args=[self.transaction_request.reference_id]), {
            # Add required fields for transaction request approval
        })
        self.assertEqual(response.status_code, 302) # Redirect to some page after successful transaction request approval
        self.transaction_request.refresh_from_db()
        self.assertEqual(self.transaction_request.status, TransactionStatus.APPROVED)

class NotificationDeletionTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notification = Notifications.objects.create(notification_for=self.user, message='Test Notification', is_read=False)

    def test_notification_deletion(self):
        # Test notification deletion
        response = self.client.post(reverse('notification_delete', args=[self.notification.reference_id]), {
            # Add required fields for notification deletion
        })
        self.assertEqual(response.status_code, 302) # Redirect to notification list view after deletion
        self.assertFalse(Notifications.objects.filter(reference_id=self.notification.reference_id).exists())
