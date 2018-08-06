from django.conf.urls import url

from django.urls import path

from . import views # import views so we can use them in urls.

app_name='catalogue'

urlpatterns = [
    path('', views.listing, name='listing'),
    path('search/', views.search, name='search'),
    path('<product_id>/', views.detail, name='detail'),
]