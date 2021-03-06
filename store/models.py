from django.db import models
from django.urls import reverse
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from  django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    
    def CategoryItems(self):
        return Item.objects.filter(category=self)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "categories"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
class Item(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name='item_category', blank = True, null=True)
    description = models.TextField(null=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=10)
    new_price = models.DecimalField(decimal_places=2, max_digits=10,blank=True, null=True)
    pic = models.ImageField(upload_to='images/items', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(550,750)],
                                   format='JPEG',
                                   options = {'quality':100})
    main_thumbnail = ImageSpecField(source='pic',
                                   processors = [ResizeToFill(440,590)],
                                   format='JPEG',
                                   options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("retechecommerce:item-detail", kwargs={"slug": self.slug})
    
    def get_add_to_cart_url(self):
        return reverse("retechecommerce:add-to-cart", kwargs={"slug": self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("retechecommerce:remove-from-cart", kwargs={"slug": self.slug})
    
    def get_add_to_wishlist(self):
        return reverse("retechecommerce:add-to-cart", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.item.name} - {self.quantity}'
    
    def totalQuantity(self):
        return self.item.new_price * self.quantity
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL,
                                        blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def totalPrice(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.totalQuantity
        return total

    
class WishListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.item.name
    
    class Meta:
        verbose_name = ('wishlist item')
        verbose_name_plural = ('Wishlist Items')
        ordering = ['-timestamp']
        unique_together = ['user', 'item']
        
    def get_absolute_url(self):
        return self.item.get_absolute_url()

class UserWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(WishListItem)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = ('Wishlist')
        verbose_name_plural = ('Wishlists')
        ordering = ['-timestamp']
        unique_together = ['user']
    
    
class Upcoming_Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=250)
    description = models.TextField(null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    pic = models.ImageField(upload_to='images/items/upcoming', default='images/items/default.png')
    pic_thumbnail = ImageSpecField(source='pic',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.names
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
class Manufacture(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200, default="#")
    logo = models.ImageField(upload_to='images/manufactures', default='images/manafactures/default.png')
    logo_thumbnail = ImageSpecField(source='logo',
                                processors = [ResizeToFill(120,45)],
                                format='JPEG',
                                options = {'quality':100})
    slug = models.SlugField(blank=True, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    phone = models.CharField(max_length=15)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    city = models.CharField(max_length=255)
    delivery_tel = models.IntegerField()
    
    def __str__(self):
        return 
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
class Coupon(models.Model):
    code = models.CharField(max_length=255)
    
    def __str__(self):
        return self.code
    
#mpesa models#

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    
    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'
        
class MpesaCallsBack(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()
    
    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'
        
class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'mpesa payment'
        verbose_name_plural = 'mpesa payments'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"