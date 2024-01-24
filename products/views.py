from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Price, Product
# Create your views here.



class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "products/product_list.html"

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = Price.objects.filter(product=self.get_object())
        return context
    



# PAYMENT VIEWS

def successPayment(request):
	return render(request, 'payment/successPayment.html')

def errorPayment(request):
	return render(request, 'payment/errorPayment.html')

def pricingPlan(request):
	return render(request, 'payment/pricing.html')



def serviceInvoice(request):
	return render(request, 'payment/serviceInvoice.html')