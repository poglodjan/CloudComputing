# backend-django/psychosphere/models.py

from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=280, unique=True, blank=True)

    excerpt = models.TextField(
        help_text="Krótki opis widoczny na karcie artykułu."
    )
    content = models.TextField()

    cover_image_url = models.URLField(blank=True)

    category = models.ForeignKey(
        Category,
        related_name="articles",
        on_delete=models.PROTECT,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
    )

    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="psychosphere_articles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="psychosphere_subscription",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.EXPIRED,
    )

    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    external_subscription_id = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} – {self.status}"