from django.conf import settings

from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateAPIView,)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import HelmetSlot
from .permissions import IsSlotModificationAllowed
from .serializers import HelmetSlotSerializer



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
        if instance.is_locked:
            instance.is_locked = False
            instance.save()
            return Response({'message': 'Unlocked'})
        else:
            if not instance.is_empty:
                instance.is_locked = True
                instance.save()
                return Response({'message': 'Locked'})
            return Response({'message': 'Please attach Helmet'})