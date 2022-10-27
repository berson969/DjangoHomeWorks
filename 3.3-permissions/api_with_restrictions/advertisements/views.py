from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .models import Advertisement, FavoriteAdvertisement
from .serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrIsStaffOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    @action(detail=False)
    def get_favorites(self, request):
        queryset = FavoriteAdvertisement.objects.filter(user=request.user)
        serializer = FavoriteAdvertisementSerializer(queryset, many=True)
        return Response({request.user.username: serializer.data})

    @action(methods=['post'], detail=True)
    def add_favorite(self, request, pk=None):
        queryset = Advertisement.objects.get(id=pk)
        if queryset:
            validated_data = {'favorite': queryset, 'user': request.user}
            serializer = FavoriteAdvertisementSerializer(data=validated_data)
            serializer.is_valid()
            serializer.validate(data=validated_data)
            serializer.create(validated_data)
            return Response("The Advertisement added to database", status=status.HTTP_201_CREATED)
        return Response('The Advertisement missing in database', status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def destroy_favorite(self, request, pk=None):
        queryset = FavoriteAdvertisement.objects.filter(favorite=pk, user=request.user)
        if queryset:
            FavoriteAdvertisement.delete(FavoriteAdvertisement.objects.get(favorite=pk, user=request.user))
            return Response('The Advertisement is removed from Favorites', status=status.HTTP_204_NO_CONTENT)
        return Response('The Advertisement missing in Favorites ', status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrIsStaffOrReadOnly()]
        return []

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            return Advertisement.objects.all()
        elif self.request.user.is_anonymous:
            return Advertisement.objects.exclude(status='DRAFT')
        return Advertisement.objects.filter(Q(creator=self.request.user) | ~Q(status='DRAFT'))
