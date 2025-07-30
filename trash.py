from django.db import models
from django.utils import timezone


# class Property(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     address = models.CharField(max_length=100)
#     price = models.DecimalField(decimal_places=2, max_digits=10)
#     availability = models.BooleanField(default=True)
#
#     def update_availability(self):
#         has_active_bookings = self.bookings.filter(is_active=True).exists()
#         if has_active_bookings:
#             self.availability = False
#             self.save()
#
#
# class Booking(models.Model):
#     property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
#     start_date = models.DateField(null=False, blank=False)
#     end_date = models.DateField(null=False, blank=False)
#     is_active = models.BooleanField(default=True)
#
#     def set_status(self):
#         today = timezone.now()
#         was_active = self.is_active
#         self.is_active = self.start_date <= today <= self.end_date
#         self.save()
#
#         if was_active != self.is_active:
#             self.property.update_availability()

from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Введите номер телефона в формате: '+999999999'. До 15 цифр."
)

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
"""
                                pip install django-phonenumber-field[phonenumbers]

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True, null=True)

"""
class Property(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    availability = models.BooleanField(default=True)

    def update_availability(self):      #попробовать сделать связь мэни(booking.is_active) ту оне(проперти.availability)"""
        has_active_bookings = self.bookings.filter(is_active=True).exists()
        if has_active_bookings:
            self.availability = False
            self.save()


class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def set_status(self):
        today = timezone.now()
        was_active = self.is_active
        self.is_active = self.start_date <= today <= self.end_date
        self.save()

        if was_active != self.is_active:
            self.property.update_availability()