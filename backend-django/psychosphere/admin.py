from django.contrib import admin

from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]

    search_fields = [
        "name",
    ]

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]

    search_fields = [
        "name",
    ]

    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "status",
        "is_premium",
        "is_featured",
        "published_at",
    ]

    list_filter = [
        "status",
        "is_premium",
        "is_featured",
        "category",
        "tags",
    ]

    search_fields = [
        "title",
        "excerpt",
        "content",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    filter_horizontal = [
        "tags",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = [
        (
            "Podstawowe informacje",
            {
                "fields": [
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "image_url",
                ]
            },
        ),
        (
            "Klasyfikacja",
            {
                "fields": [
                    "category",
                    "tags",
                ]
            },
        ),
        (
            "Dostęp i publikacja",
            {
                "fields": [
                    "read_time_minutes",
                    "is_premium",
                    "is_featured",
                    "status",
                    "published_at",
                ]
            },
        ),
        (
            "Informacje techniczne",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]