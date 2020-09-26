from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter


router1 = DefaultRouter()

router1.register('restoran/(?P<r_id>\d+)', TableViewSet, basename="restoran_tables" )


urlpatterns = [
    path('', include(router1.urls)),
    path('restoran/<int:r_id>/tables', New_RestoranTablesViewSet.as_view(), name="restoran_tables_worker"),
    path('restoran/<int:r_id>/table/<int:t_n>/done_order', CookViewSet.as_view(), name="done_order"),
    path('profile/<int:w_id>/token', WorkerProfileViewSet.as_view(), name="worker_profile"),
    path('profile/<int:w_id>/edit/password/token', WorkerEditPassword.as_view(), name="worker_profile"),
    path('restoran/<int:r_id>/tables/<int:t_n>', New_RestoranTableDetailViewSet.as_view(), name="restoran_table_detail_worker"),
]

