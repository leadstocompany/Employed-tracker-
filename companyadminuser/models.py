from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from main.models import *
from random import randint

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if Category.objects.filter(name=self.name).exists():
            extra = str(randint(1, 10000))
            self.slug = slugify(self.name) + "-" + extra
        else:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class ContactCategory(models.Model):
    contact = models.ForeignKey(ContactDetails, on_delete=models.CASCADE, blank=True, null=True)
    cats = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

