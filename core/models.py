from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='upload/rest-image/')
    mobile_number = models.CharField(max_length=13)
    delivery_cost = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    item = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    menu_items = models.ManyToManyField(MenuItem, related_name='menus')

    def __str__(self):
        return f'Menu of {self.restaurant.name}'

class OrderRequest(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="order_requests")
    order_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_requests_made")
    order_receivers = models.ManyToManyField(User, related_name="received_order_requests", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    total_cost = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Order by {self.order_maker} at {self.restaurant.name}"


class OrderItem(models.Model):
    order_request = models.ForeignKey(OrderRequest, on_delete=models.CASCADE, related_name="order_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items_added")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_cost = models.FloatField(default=0.0)  

    def save(self, *args, **kwargs):
        self.item_cost = self.menu_item.price * self.quantity  
        super().save(*args, **kwargs)  