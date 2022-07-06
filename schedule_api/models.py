from django.db import models
from django.conf import settings
from schedule_users.models import DriverProfile, PassengerProfile, User

DeUser = settings.AUTH_USER_MODEL
# Create your models here.

NOTIFICATIONS_STATUS = (
    ("Read", "Read"),
    ("Not Read", "Not Read"),
)

NOTIFICATIONS_TRIGGERS = (
    ("Triggered", "Triggered"),
    ("Not Triggered", "Not Triggered"),
)

DRIVER_STATUS = (
    ("Booked", "Booked"),
    ("Not Booked", "Not Booked"),
)

ACCEPT_SCHEDULE_RIDE = (
    ("Accept", "Accept"),
    ("Reject", "Reject"),
)
ACCEPT_RIDE_STATUS = (
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
)

SCHEDULE_RIDE_OPTIONS = (
    ("One Time", "One Time"),
    ("Daily", "Daily"),
    ("Days", "Days"),
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
)

DRIVER_PAYMENT_CONFIRMATION = (
    ("Confirmed", "Confirmed"),
    ("Not Confirmed", "Not Confirmed"),
)
SCHEDULE_TYPES = (
    ("One Time", "One Time"),
    ("Daily", "Daily"),
    ("Days", "Days"),
    ("Weekly", "Weekly"),
    ("Until Cancelled", "Until Cancelled"),
)

SCHEDULE_PRIORITY = (
    ("High", "High"),
    ("Low", "Low"),
)


# working and functioning now models
class ScheduleRide(models.Model):
    passenger = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="passenger_scheduling_ride")
    driver = models.ForeignKey(DeUser, on_delete=models.CASCADE)
    schedule_title = models.CharField(max_length=255, default="")
    schedule_type = models.CharField(max_length=255, default="One Time", choices=SCHEDULE_TYPES)
    schedule_priority = models.CharField(max_length=255, default="High", choices=SCHEDULE_PRIORITY)
    schedule_description = models.TextField(default="", )
    pickup_location = models.CharField(max_length=255, blank=True, )
    drop_off_location = models.CharField(max_length=255, blank=True, )
    pick_up_time = models.CharField(max_length=100, blank=True, )
    pick_up_date = models.CharField(max_length=100, blank=True, )
    completed = models.BooleanField(default=False)
    scheduled = models.BooleanField(default=False)
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=00.00)
    initial_payment = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=00.00)
    date_scheduled = models.DateField(auto_now_add=True)
    time_scheduled = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.schedule_title)

    def get_driver_profile_pic(self):
        my_driver = DriverProfile.objects.get(user=self.driver)
        if my_driver:
            return "https://taxinetghana.xyz" + my_driver.profile_pic.url
        return ""

    def get_passenger_profile_pic(self):
        my_passenger = PassengerProfile.objects.get(user=self.passenger)
        if my_passenger:
            return "https://taxinetghana.xyz" + my_passenger.profile_pic.url
        return ""


class Messages(models.Model):
    ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE, related_name="Ride_receiving_messages")
    user = models.ForeignKey(DeUser, on_delete=models.CASCADE)
    message = models.TextField()
    time_sent = models.TimeField(auto_now_add=True)
    date_sent = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.ride

    def get_profile_pic(self):
        de_user = User.objects.get(username=self.user.username)
        if de_user.user_type == 'Passenger':
            my_passenger = PassengerProfile.objects.get(user=self.ride.passenger)
            if my_passenger:
                return "https://taxinetghana.xyz" + my_passenger.profile_pic.url
            return ""

        if de_user.user_type == 'Driver':
            my_driver = DriverProfile.objects.get(user=self.ride.driver)
            if my_driver:
                return "https://taxinetghana.xyz" + my_driver.profile_pic.url
            return ""


class AcceptedScheduledRides(models.Model):
    scheduled_ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE)
    driver = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="driver_accepting_scheduled_ride")
    date_accepted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver} accepted ride {self.scheduled_ride.id}"


class RejectedScheduledRides(models.Model):
    scheduled_ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE)
    driver = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="driver_rejecting_scheduled_ride")
    date_rejected = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver} rejected ride {self.scheduled_ride.id}"


class BidScheduleRide(models.Model):
    scheduled_ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE, related_name="Scheduled_Ride_to_accept")
    user = models.ForeignKey(DeUser, on_delete=models.CASCADE)
    bid = models.DecimalField(blank=True, decimal_places=2, max_digits=10, default=00.00)
    date_accepted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bid)

    def get_profile_pic(self):
        deUser = User.objects.get(username=self.user.username)
        if deUser.user_type == 'Passenger':
            my_passenger = PassengerProfile.objects.get(user=self.scheduled_ride.passenger)
            if my_passenger:
                return "https://taxinetghana.xyz" + my_passenger.profile_pic.url
            return ""

        if deUser.user_type == 'Driver':
            my_driver = DriverProfile.objects.get(user=self.scheduled_ride.driver)
            if my_driver:
                return "https://taxinetghana.xyz" + my_driver.profile_pic.url
            return ""


class CompletedBidOnScheduledRide(models.Model):
    scheduled_ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE)
    driver = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="driver_completing_scheduled_ride")
    date_accepted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid on ride {self.scheduled_ride.id} is complete"


class CompletedScheduledRides(models.Model):
    scheduled_ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE)
    date_completed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.scheduled_ride.id} is complete"


class ScheduledNotifications(models.Model):
    notification_id = models.CharField(max_length=100, blank=True, default="")
    notification_tag = models.CharField(max_length=255, blank=True, default="")
    notification_title = models.CharField(max_length=255, blank=True)
    notification_message = models.TextField(blank=True)
    read = models.CharField(max_length=20, choices=NOTIFICATIONS_STATUS, default="Not Read")
    notification_trigger = models.CharField(max_length=255, choices=NOTIFICATIONS_TRIGGERS, default="Triggered",
                                            blank=True)
    notification_from = models.ForeignKey(DeUser, on_delete=models.CASCADE, null=True)
    notification_to = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="DeUser_receiving_notification",
                                        null=True)
    passengers_pickup = models.CharField(max_length=255, null=True, blank=True)
    passengers_dropOff = models.CharField(max_length=255, null=True, blank=True)
    schedule_ride_id = models.CharField(max_length=255, blank=True)
    schedule_ride_accepted_id = models.CharField(max_length=255, blank=True)
    schedule_ride_rejected_id = models.CharField(max_length=255, blank=True)
    completed_schedule_ride_id = models.CharField(max_length=255, blank=True)
    message_id = models.CharField(max_length=255, blank=True, default='')
    complain_id = models.CharField(max_length=255, blank=True)
    reply_id = models.CharField(max_length=255, blank=True)
    review_id = models.CharField(max_length=255, blank=True)
    rating_id = models.CharField(max_length=255, blank=True)
    payment_confirmed_id = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_title

    def get_passengers_notification_from_pic(self):
        my_user = User.objects.get(username=self.notification_from.username)
        if my_user.user_type == "Passenger":
            my_passenger = PassengerProfile.objects.get(user=self.notification_from)
            if my_passenger:
                return "https://taxinetghana.xyz" + my_passenger.profile_pic.url
            return ""


class DriverAnnounceArrival(models.Model):
    ride = models.ForeignKey(ScheduleRide, on_delete=models.CASCADE)
    driver = models.ForeignKey(DeUser, on_delete=models.CASCADE, related_name="driver_announcing_arrival")
    date_announced = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver} accepted ride {self.ride.id}"
# working and functioning now models
