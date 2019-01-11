from django.urls import path

from . import views

app_name = 'commerce'

urlpatterns = [
    path('<str:version>/', views.itemList, name='itemlist'),
    path('<str:version>/<str:name>', views.detailItem, name='detailitem'),

]
