# from django.core.validators import MinValueValidator
from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


# from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # print(positions)
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.get_or_create(stock=stock, **position)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        # print(instance, validated_data)
        for position in positions:
            # print(position['product'], position['quantity'], position['price'])
            # defaults = StockProduct.objects.filter(stock=stock, product=position['product'])
            # if defaults:
            #     print(defaults[0].quantity)
            # print(defaults)
            update_product = StockProduct.objects.update_or_create(stock=stock, **position)
            print(update_product)
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def validate_positions(self, value):
        if not value:
            raise serializers.ValidationError("Не указаны позиции заказа")
        product_ids = [item['product'].id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Дублируются позиции в заказе")
        return value

    def validate(self, attrs):
        print(attrs)
        return attrs
