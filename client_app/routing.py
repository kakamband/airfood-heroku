from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/restoran/(?P<restoran_id>\d+)/table/(?P<table_number>\d+)/$', consumers.TableConsumer),
]
