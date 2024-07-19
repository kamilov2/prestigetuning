from rest_framework import serializers
from main.models import Product, Brand, CarModel, Category

class ProductSerializer(serializers.ModelSerializer):
    image_1 = serializers.SerializerMethodField()
    uzs_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    usd_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name','brand', 'car_model','category','ceiling_price', 'image_1', 'uzs_price', 'usd_price']

    def get_image_1(self, obj):
        request = self.context.get('request')
        if request and obj.image_1:
            return request.build_absolute_uri(obj.image_1.url)
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name']


class ProductDetailSerializer(serializers.ModelSerializer):
    image_1 = serializers.SerializerMethodField()
    image_2 = serializers.SerializerMethodField()
    image_3 = serializers.SerializerMethodField()
    image_4 = serializers.SerializerMethodField()
    brand = BrandSerializer()
    car_model = CarModelSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'brand', 'car_model', 
            'category', 'image_1', 'image_2', 'image_3', 'image_4', 
            'usd_price', 'uzs_price'
        ]

    def get_image_1(self, obj):
        request = self.context.get('request')
        if request and obj.image_1:
            return request.build_absolute_uri(obj.image_1.url)
        return None

    def get_image_2(self, obj):
        request = self.context.get('request')
        if request and obj.image_2:
            return request.build_absolute_uri(obj.image_2.url)
        return None

    def get_image_3(self, obj):
        request = self.context.get('request')
        if request and obj.image_3:
            return request.build_absolute_uri(obj.image_3.url)
        return None

    def get_image_4(self, obj):
        request = self.context.get('request')
        if request and obj.image_4:
            return request.build_absolute_uri(obj.image_4.url)
        return None