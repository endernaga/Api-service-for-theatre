from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name='plays')
    genres = models.ManyToManyField(Genre, related_name='genres')

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Performance(models.Model):
    plays = models.ForeignKey(Play, related_name='performances', on_delete=models.CASCADE)
    theatre = models.ForeignKey(TheatreHall, related_name='performances', on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), related_name="reservations", on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, related_name='tickets', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name='tickets', on_delete=models.CASCADE)
