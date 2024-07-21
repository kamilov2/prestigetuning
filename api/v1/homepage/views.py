import telebot
from rest_framework import viewsets, views, status
from main.models import Banner, Category, Product
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.db.models import Prefetch, Count, Avg
from .serializers import BannerSerializer, CategorySerializer, TopSellingProductsSerializer, RecommendedProductsSerializer, ContactSerializer

bot = telebot.TeleBot('6704792126:AAGpqxtc36goOtl62kKQpCSXEzp9d2sQ-iY')

class BannerViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().only('name', 'image', 'ceiling', 'description').order_by('?')[:3]

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related(
        Prefetch('products', queryset=Product.objects.select_related('brand', 'car_model'))
    )

class TopSellingProductsView(viewsets.ViewSet):
    def list(self, request):
        top_selling_products = Product.objects.annotate(total_sales=Count('order_items__quantity')).order_by('-total_sales')[:3]
        most_sold_product = Product.objects.annotate(total_sales=Count('order_items__quantity')).order_by('-total_sales').first()
        
        new_products_categories = Category.objects.annotate(new_products_count=Count('products')).order_by('-new_products_count')[:3]
        
        data = {
            'top_selling_products': top_selling_products,
            'most_sold_product': most_sold_product,
            'new_products_categories': new_products_categories, 
        }
        
        serializer = TopSellingProductsSerializer(data, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

class RecommendedProductsView(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]

    def list(self, request):
        recommended_products = Product.objects.annotate(avg_sell_count=Avg('sell_count')).order_by('-avg_sell_count')[:10]
        new_products_categories = Product.objects.order_by('-created')[:10]
        data = {
            'recommended_products': recommended_products,
            'new_products': new_products_categories,
        }
        serializer = RecommendedProductsSerializer(data, context={'request': request})
        return Response(serializer.data, status=HTTP_200_OK)

class ContactAPIView(views.APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            phone_number = serializer.validated_data.get('phone')
            message_text = (
                f"<b>#Bog'lanish:</b>\n\n"
                f"<b>Ism:</b> {name}\n"
                f"<b>Telefon raqami:</b> +{phone_number}\n"
            )
            bot.send_message('-1002165196907', message_text, parse_mode='html')

            return Response({"message": "Tez orada siz bilan bo'g'lanamiz"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
