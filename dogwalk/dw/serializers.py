from rest_framework import serializers

from dw.models import Pet, User, WalkOrder, Walker
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "phone"]


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ["id", "name"]


class WalkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walker
        fields = ["id", "name"]


class WalkOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    pet = PetSerializer()
    walker = WalkerSerializer()

    class Meta:
        model = WalkOrder
        fields = ["id", "user", "pet", "walker", "start_time", "end_time", "comment"]

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        walker_name = data.get("walker").get("name")

        if start_time >= end_time:
            raise serializers.ValidationError(
                "Время начала прогулки не может быть больше времени окончания."
            )

        if start_time.minute not in [0, 30]:
            raise serializers.ValidationError(
                "Прогулки должны начинаться в начале часа или в середине часа."
            )

        if end_time > start_time + timezone.timedelta(minutes=30):
            raise serializers.ValidationError(
                "Прогулка не может длиться больше чем 30 минут."
            )

        earliest_start = start_time.replace(hour=7, minute=0, second=0, microsecond=0)
        latest_start = start_time.replace(hour=23, minute=0, second=0, microsecond=0)

        if start_time < earliest_start or start_time > latest_start:
            raise serializers.ValidationError(
                "Прогулки не могут начинаться раньше 7 утра или после 11 вечера."
            )

        if WalkOrder.objects.filter(start_time=start_time, walker__name=walker_name).exists():
            raise serializers.ValidationError(
                f"У {walker_name} на это время уже назначена прогулка."
            )

        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        pet_data = validated_data.pop("pet")
        walker = validated_data.pop("walker")

        user, _ = User.objects.get_or_create(**user_data)
        pet, _ = Pet.objects.get_or_create(user=user, **pet_data)
        walker, _ = Walker.objects.get_or_create(**walker)

        return WalkOrder.objects.create(
            user=user, pet=pet, walker=walker, **validated_data
        )
