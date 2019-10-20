from rest_framework import serializers

from .models import HelmetSlot


class HelmetSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelmetSlot
        fields = ('id', 'is_empty', 'is_locked',)


# class HelmetSlotSerializer(serializers.Serializer):
#     helmet_slot = serializers.PrimaryKeyRelatedFie