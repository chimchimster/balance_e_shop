from . import views
from django.urls import path


app_name = 'coupon'


urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
]