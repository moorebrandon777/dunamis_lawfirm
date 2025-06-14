from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField

# main/models.py
class Attorney(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    practice_area = models.CharField(max_length=200)
    bio = models.TextField()
    photo = CloudinaryField('image', null=True, default=None, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    linkedin_url = models.URLField(null=True, blank=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    seo_title = models.CharField(max_length=255, blank=True, help_text="SEO title")
    seo_description = models.CharField(max_length=500, blank=True, help_text="SEO meta description")
    seo_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords")
    flaticon = models.CharField(max_length=50, blank=True, help_text="for flaticon icon after the -")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('frontend:service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

