from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'cov19diff'

router = routers.DefaultRouter()
router.register(r'dailycsvs', views.DailyCsvViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('dodiff', views.dodiff, name='dodiff'),
    path('list/<str:old>/<str:new>', views.difflist, name='list'),
    path('dayly/<str:day>/<str:ord>', views.daylyStat, name='dayly'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
