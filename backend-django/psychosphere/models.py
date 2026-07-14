from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=60,
        unique=True,
    )

    slug = models.SlugField(
        max_length=70,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Szkic"
        PUBLISHED = "published", "Opublikowany"
        ARCHIVED = "archived", "Zarchiwizowany"

    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
    )

    author = models.CharField(
        max_length=150,
        default="Redakcja PsychSphere",
        help_text="Imię i nazwisko autora wyświetlane przy artykule.",
    )

    excerpt = models.TextField(
        help_text="Krótki opis wyświetlany na karcie artykułu.",
    )

    content = models.TextField(
        help_text="Pełna treść artykułu. Oddzielaj akapity pustą linią.",
    )

    image_url = models.URLField(
        max_length=1000,
        blank=True,
        help_text="Adres URL zdjęcia wyświetlanego na karcie.",
    )

    categories = models.ManyToManyField(
        Category,
        related_name="articles",
        verbose_name="Kategorie",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
    )

    read_time_minutes = models.PositiveSmallIntegerField(
        default=5,
    )

    is_premium = models.BooleanField(
        default=False,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    published_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Artykuł"
        verbose_name_plural = "Artykuły"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.title) or "artykul"
        candidate = base_slug
        number = 2

        while Article.objects.exclude(pk=self.pk).filter(
            slug=candidate
        ).exists():
            candidate = f"{base_slug}-{number}"
            number += 1

        return candidate

    def __str__(self):
        return self.title