from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name='home'),
    path('add_owner',views.add_owner,name='add_owner'),
    path('view_owner',views.view_owner,name='view_owner'),
    path('login',views.login,name='login'),
    path('owner_home',views.owner_home,name='owner_home'),
    path('add_hotel',views.add_hotel,name='add_hotel'),
]
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


