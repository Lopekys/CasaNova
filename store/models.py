from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    country = CountryField(blank_label="(select country)", null=True, blank=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    state_or_country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Delivered', 'Delivered')],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


class Subscribe(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)


class Testimonial(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/', blank=True)

    def __str__(self):
        return f"{self.name} ({self.position})"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='blog/')
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
