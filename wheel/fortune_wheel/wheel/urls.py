from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wheel/', views.wheel_view, name='wheel'),
    path('spin/', views.spin_wheel, name='spin'),
    path('profile/', views.profile_view, name='profile'),
    path('shop/', views.shop_view, name='shop'),
    path('buy/<int:item_id>/', views.buy_item, name='buy'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
