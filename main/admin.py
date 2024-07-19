from django.contrib import admin
from .models import Banner, Category, Product, Order, OrderItem, Brand, CarModel




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    max_num = 4

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_id']
    search_fields = ['name']
    readonly_fields = ['category_id']
    inlines = [ProductInline]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'ceiling', 'created', 'updated']
    search_fields = ['name']
    list_filter = ['created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'usd_price', 'uzs_price', 'count_in_stock', 'created', 'updated']
    list_filter = ['category', 'created']
    search_fields = ['name']
    readonly_fields = ['sell_count']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'full_name', 'phone_number', 'delivery_status', 'created', 'updated']
    list_filter = ['delivery_status', 'created']
    search_fields = ['full_name', 'phone_number', 'address']
    date_hierarchy = 'created'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity', 'get_total_price']
    list_filter = ['order__created']
    search_fields = ['order__full_name', 'product__name']
    readonly_fields = ['get_total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']
    readonly_fields = ['id']

@admin.register(CarModel)   
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']
    readonly_fields = ['id']

admin.site.register(Category, CategoryAdmin)
