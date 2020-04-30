from django.urls import path

from . import views

app_name = 'cov19diff'

urlpatterns = [
    path('', views.index, name='index'),
    path('dodiff', views.dodiff, name='dodiff'),
    path('list/<str:old>/<str:new>', views.difflist, name='list'),
    path('dayly/<str:day>/<str:ord>', views.daylyStat, name='dayly'),
]
