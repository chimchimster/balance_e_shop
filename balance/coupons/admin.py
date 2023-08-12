from .models import Coupon
from django.contrib import admin


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active',)
    list_filter = ('active', 'valid_from', 'valid_to',)
    search_fields = ('code',)


admin.site.register(Coupon, CouponAdmin)