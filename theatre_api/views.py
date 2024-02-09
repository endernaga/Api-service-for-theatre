from django.shortcuts import render
from rest_framework import viewsets

from theatre_api.models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation
from theatre_api.serializer import GenreSerializer, ActorSerializer, PlaySerializer, PlayListSerializer, \
    PlayDetailSerializer, TheatreHallSerializer, PerformanceSerializer, PerformanceDetailSerializer, \
    PerformanceListSerializer, TicketSerializer, TicketListSerializer, ReservationSerializer, \
    ReservationListSerializer, ReservationDetailSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all().prefetch_related("actors", "genres")
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PlaySerializer
        if self.action == "retrieve":
            return PlayDetailSerializer
        return PlayListSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().select_related("plays", "theatre")
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        if self.action == "create":
            return PerformanceSerializer
        return PerformanceListSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).prefetch_related("tickets").prefetch_related("tickets__performance__plays", "tickets__performance__theatre")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        if self.action == "retrieve":
            return ReservationDetailSerializer
        return ReservationSerializer

