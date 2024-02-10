from django.contrib import admin

from theatre_api.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)

models_list = [
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
]

for model in models_list:
    admin.site.register(model)
