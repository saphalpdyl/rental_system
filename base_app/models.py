import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


def generate_uuid():
    return uuid.uuid4().hex  # 'asdawdsdwadadasdasawda'


class ApplicationUser(AbstractUser):
    user_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    phone_no = models.CharField(max_length=12)
    profile_picture = models.ImageField(upload_to="uploads/", null=True, blank=True)
    is_renter = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class RenterUser(models.Model):
    renter_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)


class AdminUser(models.Model):
    admin_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)


class BaseClass(models.Model):
    reference_id = models.CharField(
        max_length=32, primary_key=True, unique=True, default=generate_uuid
    )
    data_generated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class RenterRegisterRequests(BaseClass):
    # Who made the request ?
    application_user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    # Is the request left to be reviewed(pending)?
    is_reviewed = models.BooleanField(default=False)


class RenterRegisterResults(BaseClass):
    # Which request ?
    renter_request = models.ForeignKey(RenterRegisterRequests, on_delete=models.CASCADE)
    # Which admin reviewed it?
    reviewed_by = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    # Was the user's request approved ?
    is_approved = models.BooleanField()


class Vehicles(BaseClass):
    owner = models.ForeignKey(RenterUser, on_delete=models.CASCADE)
    price = models.FloatField()
    vehicle_name = models.CharField(max_length=32)
    vehicle_desc = models.TextField(null=True, blank=True)
    vehicle_company = models.CharField(max_length=30)
    vehicle_type = models.CharField(max_length=15)
    vehicle_seater = models.PositiveSmallIntegerField()
    vehicle_number_plate = models.CharField(max_length=15, unique=True)
    vehicle_documents = models.ImageField(upload_to="uploads/", null=True, blank=True)
    vehicle_description_image = models.ImageField(
        upload_to="uploads/", null=True, blank=True
    )
    is_available = models.BooleanField(default=True)
    can_be_listed = models.BooleanField(default=False)

    def __str__(self):
        return self.vehicle_name


class VehicleListingRequests(BaseClass):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    is_reviewed = models.BooleanField(default=False)


class Notifications(BaseClass):
    notification_for = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)  # Main title
    desc = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)


# Enums
class RentingStatus(models.TextChoices):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class VehicleRentingRequests(BaseClass):
    buyer = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name='renting_requests')
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, related_name='renting_requests')
    # Rent for how many days?
    renting_period = models.PositiveIntegerField()
    status = models.TextField(choices=RentingStatus)