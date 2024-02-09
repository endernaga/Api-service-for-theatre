from django.db import transaction
from rest_framework import serializers

from theatre_api.models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayListSerializer(PlaySerializer):
    actors = serializers.StringRelatedField(read_only=True, many=True)
    genres = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)

    class Meta:
        model = Play
        fields = PlaySerializer.Meta.fields


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "plays", "theatre", "show_time")


class PerformanceDetailSerializer(PerformanceSerializer):
    plays = PlayDetailSerializer(read_only=True)
    theatre = TheatreHallSerializer(read_only=True)

    class Meta:
        model = Performance
        fields = PerformanceSerializer.Meta.fields


class PerformanceListSerializer(PerformanceSerializer):
    film_title = serializers.SlugRelatedField(source="plays", slug_field="title", read_only=True)
    theatre_name = serializers.SlugRelatedField(source="theatre", slug_field="name", read_only=True)

    class Meta:
        model = Performance
        fields = ("id", "film_title", "theatre_name", "show_time")


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        Ticket.validate_seat(attrs["seat"], attrs["performance"].theatre.seats_in_row, serializers.ValidationError)
        Ticket.validate_row(attrs["row"], attrs["performance"].theatre.rows, serializers.ValidationError)

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")
        read_only_fields = ("id",)


class TicketListSerializer(TicketSerializer):
    performance = PerformanceListSerializer(read_only=True)


class TakenSeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservations = Reservation.objects.create(**validated_data)
            for ticket in tickets_data:
                Ticket.objects.create(reservation=reservations, **ticket)
            return reservations


class ReservationListSerializer(ReservationSerializer):
    performance_title = serializers.SerializerMethodField(read_only=True)
    theatre = serializers.SerializerMethodField(read_only=True)
    show_time = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_performance_title(reservation):
        return [f"{count + 1}: {ticket.performance.plays.title}" for count, ticket in enumerate(reservation.tickets.all())]

    @staticmethod
    def get_theatre(reservation):
        return [f"{count + 1}: {ticket.performance.theatre.name}" for count, ticket in enumerate(reservation.tickets.all())]

    @staticmethod
    def get_show_time(reservation):
        return [f"{count + 1}: {ticket.performance.show_time}" for count, ticket in
                enumerate(reservation.tickets.all())]

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "theatre", "performance_title", "show_time")


class ReservationDetailSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
