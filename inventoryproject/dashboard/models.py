from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CAREGORY = (
    ('Headphones', 'Headphones'),
    ('Game Console', 'Game Console'),
    ('Phone', 'Phone'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CAREGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)
    
    class Meta:
        verbose_name_plural = 'Product' # to change the name of the model in the admin panel
    
    def __str__(self):
        return f'{self.name}'
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Order' # to change the name of the model in the admin panel
    
    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'
