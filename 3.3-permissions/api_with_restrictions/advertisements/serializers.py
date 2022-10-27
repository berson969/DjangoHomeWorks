from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        count = Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN').count()
        if count >= 10 and (data.get('status') == 'OPEN' or self.context["request"].method == 'POST'):
            raise ValidationError("Exceeded max number of opening advertisements")
        return data


class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    favorite = AdvertisementSerializer(
        read_only=False,
    )

    class Meta:
        model = FavoriteAdvertisement
        # depth = 1
        fields = ['favorite', 'user']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # data.update(...)
    #     return data

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        if FavoriteAdvertisement.objects.filter(user=data['user'], favorite=data['favorite']):
            raise ValidationError('The Advertisement already is favorite')
        if data['favorite'].creator == data['user']:
            raise ValidationError("There is owner's advertisement")
        return data
