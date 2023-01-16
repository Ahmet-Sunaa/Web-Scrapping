from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("products/",views.view_products,name='products'),
    path("allproducts/",views.view_all_products,name='allproducts'),
    path("feature/<int:id>/",views.feature,name='feature'),
    path("category/<str:brand>/",views.category_by_brand,name='category_by_brand'),
    path("category/<str:size>/",views.category_by_size,name='category_by_size'),
    path("category/<str:os>/",views.category_by_os,name='category_by_os'),
]