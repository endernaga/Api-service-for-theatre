from django.urls import path, include
from rest_framework import routers

from theatre_api.views import ActorViewSet, GenreViewSet, PlayViewSet, TheatreHallViewSet, PerformanceViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("theatre-hall", TheatreHallViewSet)
router.register("performance", PerformanceViewSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "theatre_api"
