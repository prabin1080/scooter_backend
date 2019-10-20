from django.urls import path, include

from .views import (HelmetSlotListAPIView, HelmetSlotRetrieveUpdateAPIView, HelmetSlotQRUpdateAPIView, BookingCountRetrieveAPIView,)


urlpatterns = [
    path('slots/', HelmetSlotListAPIView.as_view()),
    path('slot/<int:pk>/', HelmetSlotRetrieveUpdateAPIView.as_view()),
    path('slot-qr/<int:pk>/', HelmetSlotQRUpdateAPIView.as_view()),
    path('booking-details/', BookingCountRetrieveAPIView.as_view()),
]