from django.contrib import admin

from .models import (
    AcceptedScheduledRides, RejectedScheduledRides, BidScheduleRide, CompletedBidOnScheduledRide,
    CompletedScheduledRides, ScheduledNotifications, DriverAnnounceArrival, Messages, ScheduleRide
)
admin.site.register(AcceptedScheduledRides)
admin.site.register(RejectedScheduledRides)
admin.site.register(BidScheduleRide)
admin.site.register(CompletedBidOnScheduledRide)
admin.site.register(CompletedScheduledRides)
admin.site.register(ScheduledNotifications)
admin.site.register(DriverAnnounceArrival)
admin.site.register(Messages)
admin.site.register(ScheduleRide)
