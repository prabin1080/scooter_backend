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
            if not booking_count.is_scooter_rented:
                return Response({'message': 'You need to book a Vogo First', 'count':booking_count.count})

            if booking_count.count > 1:
                return Response({'message': 'You have already have two helmets', 'count':booking_count.count})
            instance.is_locked = False
            instance.save()
            booking_count.count += 1
            booking_count.save()
            return Response({'message': 'Please collect the helmet', 'count':booking_count.count})
        else:
            if not instance.is_empty:
                instance.is_locked = True
                instance.save()
                booking_count.count -= 1
                booking_count.save()
                return Response({'message': 'Helmet is Locked', 'count':booking_count.count})
            return Response({'message': 'Please attach Helmet'})



class BookingCountRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BookingCountSerializer
    queryset = BookingCount.objects.all()

    def get_object(self):
        booking_count, created = BookingCount.objects.get_or_create(user__id=1)
        return booking_count

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        print(instance.count)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['is_scooter_rented'] == False:
            if instance.count > 0:
                return Response({'message': 'Please keep helmets back'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)