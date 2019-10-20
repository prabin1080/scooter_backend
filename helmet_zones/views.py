from django.conf import settings

from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import HelmetSlot, BookingCount
from .permissions import IsSlotModificationAllowed
from .serializers import HelmetSlotSerializer, BookingCountSerializer



class HelmetSlotListAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = HelmetSlotSerializer
    queryset = HelmetSlot.objects.all()


class HelmetSlotRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, IsSlotModificationAllowed,)
    serializer_class = HelmetSlotSerializer
    queryset = HelmetSlot.objects.all()


class HelmetSlotQRUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, IsSlotModificationAllowed,)
    serializer_class = HelmetSlotSerializer
    queryset = HelmetSlot.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        booking_count, created = BookingCount.objects.get_or_create(user__id=1)
        if instance.is_locked:
            instance.is_locked = False
            instance.save()
            booking_count.count += 1
            booking_count.save()
            return Response({'message': 'Unlocked', 'booking_count':booking_count.count})
        else:
            if not instance.is_empty:
                instance.is_locked = True
                instance.save()
                booking_count.count -= 1
                booking_count.save()
                return Response({'message': 'Locked', 'booking_count':booking_count.count})
            return Response({'message': 'Please attach Helmet'})



class BookingCountRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BookingCountSerializer
    queryset = BookingCount.objects.all()

    def get_object(self):
        booking_count, created = BookingCount.objects.get_or_create(user__id=1)
        return booking_count