from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    plays = models.ForeignKey(Play, related_name='performances', on_delete=models.CASCADE)
    theatre = models.ForeignKey(TheatreHall, related_name='performances', on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.plays.title} in {self.theatre.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), related_name="reservations", on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, related_name='tickets', on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name='tickets', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('row', 'seat', "performance")

    @staticmethod
    def validate_seat(seat: int, num_seat: int, error_to_raise):
        if not (1 <= seat <= num_seat):
            raise error_to_raise({
                "seat": f"Seat must be in range [1, {num_seat} not {seat}"
            })

    @staticmethod
    def validate_row(row: int, num_rows: int, error_to_raise):
        if not (1 <= row <= num_rows):
            raise error_to_raise({
                "row": f"Row must be in range [1, {num_rows} not {row}"
            })

    def clean(self):
        self.validate_seat(self.seat, self.performance.theatre.seats_in_row, ValidationError)
        self.validate_row(self.row, self.performance.theatre.rows, ValidationError)
