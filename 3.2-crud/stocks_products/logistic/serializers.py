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
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.get_or_create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position in positions:
            current_product = StockProduct.objects.filter(stock=stock, product=position['product'])
            if current_product:
                sum_quantity = position['quantity'] + current_product[0].quantity
                adv_price = ((position['price'] * position['quantity'])
                             + (current_product[0].price * current_product[0].quantity)) / sum_quantity
                defaults = dict(quantity=sum_quantity, price=adv_price)
            else:
                defaults = dict(quantity=position['quantity'], price=position['price'])
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults=defaults
            )
        return stock
