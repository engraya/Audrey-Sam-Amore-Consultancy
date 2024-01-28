from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


User = settings.AUTH_USER_MODEL

class ProductTag(models.Model):
    name = models.CharField(max_length=100, help_text=_("Designates the name of the tag."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    product_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    desc = models.TextField(_("Description"), blank=True)
    url = models.URLField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product.name} {self.price}"
    


class PaymentHistory(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, _("pending")),
        (COMPLETED, _("completed")),
        (FAILED, _("failed")),
    )

    email = models.EmailField(unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
