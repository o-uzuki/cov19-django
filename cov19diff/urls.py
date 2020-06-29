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
    #path('dayly/<str:day>/<str:ord>', views.daylyStat, name='dayly'),
    path('dayly',views.doDayly, name="dodayly"),
    path('dailyjson',views.getDailyJson, name="getDailyJson"),
    path('dailyjson/<str:day>/<str:ord>',views.dailyJson, name="dailyJson"),
    path('daylychart',views.doDaylyChart, name="dodaylychart"),
    path('diffdb',views.diffFromDb, name="diffFromDb"),
    path('diffjson',views.getDiffJson, name="getdiffJson"),
    path('diffjson/<str:day>',views.diffJson, name="diffJson"),
    path('dsdata', views.getDsdata, name="getDsdata"),
    path('ts/<str:cname>',views.doTS, name="doTS"),
    path('tsjson/<str:cname>',views.TSJson, name="TSJson"),
    path('test',views.test, name="test"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
