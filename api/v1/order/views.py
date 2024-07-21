import telebot
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, InvalidOperation
from main.models import Order, OrderItem, Product

bot = telebot.TeleBot('6704792126:AAGpqxtc36goOtl62kKQpCSXEzp9d2sQ-iY')

class OrderViewSet(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        city = request.data.get('city')
        village = request.data.get('village')
        street = request.data.get('street')
        home_number = request.data.get('home_number')
        delivery_status = request.data.get('delivery_status')
        message_for_delivery = request.data.get('message_for_delivery')
        items = request.data.get('items')

        if delivery_status:
            message_text = (
                f"<b>#dostavka:</b>\n\n"
                f"<b>Ism:</b> {full_name}\n"
                f"<b>Telefon raqami:</b> +{phone_number}\n"
                f"<b>Shahar:</b> {city}\n"
                f"<b>Tuman:</b> {village}\n"
                f"<b>Ko'cha:</b> {street}\n"
                f"<b>Uy:</b> {home_number}\n"
                f"<b>Yetkazib beruvchi uchun komentariy:</b> {message_for_delivery}\n\n"
                f"<b>Tovarlar:</b>\n"
            )
        else:
            message_text = (
                f"<b>#olib_ketish:</b>\n\n"
                f"<b>Ism:</b> {full_name}\n"
                f"<b>Telefon raqami:</b> +{phone_number}\n"
                f"<b>Tovarlar:</b>\n"
            )

        total_usd = Decimal('0.00')
        total_uzs = Decimal('0.00')

        product_ids = [item['id'] for item in items]
        products = Product.objects.filter(id__in=product_ids)

        product_dict = {product.id: product for product in products}

        for item in items:
            product = product_dict.get(item['id'])
            if not product:
                return Response(
                    {'error': f'Product with id {item["id"]} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            quantity = item['quantity']
            usd_price = product.usd_price or Decimal('0.00')
            uzs_price = product.uzs_price or Decimal('0.00')
            
            try:
                total_item_usd = quantity * usd_price
                total_item_uzs = quantity * uzs_price
            except InvalidOperation:
                return Response(
                    {'error': 'Invalid price format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            message_text += (
                f"- {product.name}: {quantity} x {usd_price} USD = {total_item_usd} USD "
                f"| {quantity} x {uzs_price} UZS = {total_item_uzs} UZS\n"
            )
            total_usd += total_item_usd
            total_uzs += total_item_uzs

        message_text += f"\n<b>Umumiy summa:</b> {total_usd:,.2f} USD / {total_uzs:,.2f} UZS"

        bot.send_message('-1002165196907', message_text, parse_mode='HTML')

        order = Order.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            city=city if delivery_status else 'none',
            village=village if delivery_status else 'none',
            street=street if delivery_status else 'none',
            home_number=home_number if delivery_status else 'none',
            delivery_status=delivery_status,
            message_for_delivery=message_for_delivery,
        )

        for item in items:
            product = product_dict.get(item['id'])
            if product:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.uzs_price or Decimal('0.00'),
                    quantity=item['quantity']
                )

        return Response({'success': 'Order created successfully'}, status=status.HTTP_201_CREATED)
