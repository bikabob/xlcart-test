from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    customer = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.username

class Categories(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_full_name(self):
        if self.parent:
            return f"{self.parent.get_full_name()} -> {self.title}"
        else:
            return self.title

    def __str__(self):
        return self.title


class Product(models.Model):
    # name = models.CharField(max_length=200)
    # material = models.CharField(max_length=200)
    # storage = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='Product/')
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    # features = models.TextField()
    # height = models.CharField(max_length=100)
    # stock = models.IntegerField(default=0)
    # warranty = models.TextField()
    # brand = models.CharField(max_length=200)
    # delivery_condition = models.TextField()
    # care_instruction = models.TextField(default="")
    # important_note = models.TextField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    assembly = models.CharField(max_length=200, blank=True, null=True)
    Dimensions = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    Board_Thickness = models.CharField(max_length=100, blank=True, null=True)
    Edge_Bending = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=200)  # Fixed typo here
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    storage = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Product/')
    # features = models.TextField()
    stock = models.IntegerField(default=0, blank=True, null=True)
    warranty = models.TextField()  # Fixed typo here
    # delivery_condition = models.TextField(blank=True, null=True)  # Fixed typo here
    care_instruction = models.TextField(default="", blank=True, null=True)  # Fixed typo here
    # important_note = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_final_price(self):
        if self.offer_price:
            return self.offer_price
        return self.price

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="galleries")
    images = models.ImageField(upload_to='group/')

    def __str__(self):
        return self.product.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return self.item.image.url

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in cart of {self.cart.user.username}"
