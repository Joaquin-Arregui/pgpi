"""tiendovirtual URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from products.views import ProductListView,EscaparateView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
from users.views import *
from .views import info

urlpatterns = [
    path('', EscaparateView.as_view(), name="index"),
    path('user/login/', views.login_view, name="login"),
    path('user/logout/', views.logout_view, name="logout"),
    path('user/register/', views.register, name="register"),
    path('admin/', admin.site.urls),
    path('product/', include('products.urls')),
    path('categories/', include('categories.urls')),
    path('cart/', include('carts.urls')),
    path('order/', include('orders.urls')),
    path('profile/', perfil ,name = "perfil"),
    path('opiniones/', include('opiniones.urls')),
    path('info/', info, name='info'),
    path('users/', include('users.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
