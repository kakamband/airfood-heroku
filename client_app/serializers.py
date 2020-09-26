from rest_framework import serializers
from .models import TableProducts

from app.models import Product, Table, UserProfile

class TableProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableProducts
        fields = ('id', 'table', 'product', 'unit', 'status',)

