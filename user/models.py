from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from store.models import Category

from PIL import Image
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

User = get_user_model()
# Create your models here.

STAFF_CATEGORIES = [
    ('CEO','CEO'),
    ('Manager','Manager'),
    ('Customer Manager','Customer Manager'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)
    
class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username} - {self.company}"
    
    def get_absolute_url(self):
        return self.user.profile.get_absolute_url()
    
    
class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=STAFF_CATEGORIES, max_length=255)
    image = models.ImageField(upload_to='images/staff/%Y/%m/%d')
    image_thumbnail = ImageSpecField(
                            source='image',
                            processors=[ResizeToFill(390,450)],
                            format='JPEG',
                            options={'quality':80})
    twitter = models.URLField()
    instagram = models.URLField()
    facebook = models.URLField()
    google_plus = models.URLField()
    
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return self.user.profile.get_absolute_url()
    
