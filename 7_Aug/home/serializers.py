from rest_framework import serializers
from home.models import Product

class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ['name','desc','price', 'discount']

    def get_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None

        return obj.sale_price