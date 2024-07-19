from rest_framework import serializers
from main.models import Banner, Category, Product

class BannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['name', 'image_url', 'ceiling', 'description']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class CategorySerializer(serializers.ModelSerializer):
    category_image = serializers.ImageField(required=False)  
    products_count = serializers.SerializerMethodField()  

    class Meta:
        model = Category
        fields = ['id', 'name', 'category_image', 'products_count'] 

    def get_products_count(self, obj):
        return obj.products.count()  

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.category_image and request:
            return request.build_absolute_uri(obj.category_image.url)
        return None
    
class ProductSerializer(serializers.ModelSerializer):
    image_1 = serializers.SerializerMethodField('get_image_url')
    uzs_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    usd_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'ceiling_price', 'image_1', 'uzs_price', 'usd_price']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image_1:
            return request.build_absolute_uri(obj.image_1.url)
        return None

class TopSellingProductsSerializer(serializers.Serializer):
    top_selling_products = ProductSerializer(many=True)
    most_sold_product = ProductSerializer()
    new_products_categories = CategorySerializer(many=True)

class RecommendedProductsSerializer(serializers.Serializer):
    recommended_products = ProductSerializer(many=True)
    new_products = ProductSerializer(many=True)

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
