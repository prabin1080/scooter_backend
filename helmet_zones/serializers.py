from rest_framework import serializers

from .models import HelmetSlot, BookingCount


class HelmetSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelmetSlot
        fields = ('id', 'is_empty', 'is_locked',)


class BookingCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCount
        fields = ('id', 'count', 'is_scooter_rented',)
        read_only_fields = ('count',)


# class HelmetSlotSerializer(serializers.Serializer):
#     helmet_slot = serializers.PrimaryKeyRelatedFie