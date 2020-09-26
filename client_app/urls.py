from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter


router1 = DefaultRouter()

router1.register('restoran/(?P<restoran_id>\d+)/table/(?P<table_number>\d+)', RestoranTablesViewSet, base_name="restoran_categoryes" )
router1.register('restoran/(?P<restoran_id>\d+)/table/(?P<table_number>\d+)/category/(?P<c_id>\d+)', ProductListViewSet, base_name="product_lists")
router1.register('restoran/(?P<restoran_id>\d+)/table/(?P<table_number>\d+)/category/(?P<c_id>\d+)/product/(?P<p_id>\d+)', ProductDetailViewSet, base_name="product_detail")


urlpatterns = [
    path('', include(router1.urls)),
    path('table/product/<int:p_t_id>/delete', DeleteTableProduct.as_view(), name="delete_table_product"),
    path('profile/<int:u_id>/token', ClientProfileViewSet.as_view(), name="client_profile"),
    path('profile/<int:u_id>/edit/password/token', ClientEditPassword.as_view(), name="client_profile"),
    path('restoran/<int:r_id>/table/<int:t_n>/list', ListTableProductsViewSet.as_view(), name="list_table_products"),
    path('<int:client_id>/history', HistoryesTableProductsViewSet.as_view() , name="history_table_products"),
    path('<int:client_id>/history/<int:h_code>', HistoryDetailTableProductsViewSet.as_view() , name="history_table_detail_products"),
    #
    path('restoran/<int:r_id>/tables', NewRestoranTablesViewSet.as_view(), name="restoran_tables_client"),
    path('restoran/<int:r_id>/tables/<int:t_n>', NewRestoranTableDetailViewSet.as_view(), name="restoran_table_detail_client"),
]

