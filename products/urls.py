from django.urls import path
from . import views

from .views import (
    ProductDetailView,
    ProductListView,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),


        
	path('success', views.successPayment, name="success"),
	path('error', views.errorPayment, name="error"),
	path('pricing', views.pricingPlan, name="pricing"),

	path('invoice', views.serviceInvoice, name="invoice"),
]