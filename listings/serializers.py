from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    # amenities = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"

    # def get_amenities(self, obj):
    #     labels = Property.AMENITY_LABELS
    #     return {labels[field]: getattr(obj, field) for field in labels}

    # def update(self, instance, validated_data):
    #     amenities = validated_data.pop('amenities', None)
    #     if amenities:
    #         reverse_labels = Property.get_reverse_amenity_labels()
    #         for key, value in amenities.items():
    #             field = reverse_labels.get(key)
    #             if field:
    #                 setattr(instance, field, value)
    #     return super().update(instance, validated_data)