from django.contrib import admin
from .models import ShopItem


class ShopItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description_short')
    list_filter = ('price',)
    search_fields = ('name', 'description')

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    description_short.short_description = 'Описание'


admin.site.register(ShopItem, ShopItemAdmin)