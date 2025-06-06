from django.contrib import admin

from .models import (
    BlogPost,
    ContactMessage,
    Customer,
    Order,
    OrderItem,
    Product,
    Subscribe,
    Testimonial,
)

admin.site.site_header = "CasaNova panel"
admin.site.site_title = "CasaNova admin"
admin.site.index_title = "Site administration"

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Subscribe)
admin.site.register(Testimonial)
admin.site.register(BlogPost)
admin.site.register(ContactMessage)
