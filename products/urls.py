from django.urls import path
from . import views
from .views import CreateStripeCheckoutSessionView
from .views import CancelView, SuccessView
from .views import StripeWebhookView
from .views import ProductDetailView,ProductListView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
	path("create-checkout-session/<int:pk>/", CreateStripeCheckoutSessionView.as_view(), name="create-checkout-session"),   
	path('success', views.successPayment, name="success"),
	path('error', views.errorPayment, name="error"),
	path('pricing', views.pricingPlan, name="pricing"),
	path('invoice', views.serviceInvoice, name="invoice"),
    path("/success", SuccessView.as_view(), name="success"),
    path("/cancel", CancelView.as_view(), name="cancel"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]