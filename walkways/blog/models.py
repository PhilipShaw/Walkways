from django.db import models

import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from PIL import Image
from PIL.ExifTags import TAGS


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return '/%s/' % self.slug

    def __str__(self):
        return self.title


class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft'),
    )

    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image_wide = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def get_exif(self):
        exif = {}
        image_data = Image.open(self.image)
        for tag, value in image_data._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value
        return exif

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def __str__(self):
        return(self.title)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name