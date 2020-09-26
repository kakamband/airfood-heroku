"""on_keeper URL Configuration

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from app.views import *

router = DefaultRouter()

router.register('create/client', ClientViewSet, base_name='create_client')
router.register('create/worker', UserViewSet, base_name='create_worker')
router.register('category',CategoryViewSet)
router.register('restorans',RestoransViewSet, base_name='restoran_lists')
router.register('products', ProductViewSet)
router.register('restoran/(?P<r_id>\d+)/products/lists', RestoranProductsViewSet, base_name='restoran_products_lists')
router.register('restoran/(?P<r_id>\d+)/category/(?P<c_id>\d+)/product/(?P<p_id>\d+)/detail', RestoranProductDetailViewSet, base_name='restoran_product_detail')
router.register('restoran/(?P<r_id>\d+)/category', CategoryListsViewSet, base_name='restoran_category_lists')
router.register('restoran/(?P<r_id>\d+)/category/(?P<c_id>\d+)/products', RsCtgProductViewSet, base_name='restoran_ctg_products_lists')
router.register('restoran/(?P<r_id>\d+)/worker/lists', WorkerListsViewSet, base_name='worker_lists')
# router.register('restoran/(?P<r_id>\d+)/worker/(?P<w_id>\d+)/detail', WorkerControlViewSet, base_name='worker_detail')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('user/login', LoginView.as_view()),
    path('user/logout', LogoutView.as_view()),
    path('admin_rest/restoran/<int:r_id>/worker/<int:w_id>/detail/', WorkerControlViewSet.as_view(), name='worker_detail'),
    path('admin_rest/', include(router.urls)),
    path('client/', include('client_app.urls')),
    path('worker/', include('worker_app.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)