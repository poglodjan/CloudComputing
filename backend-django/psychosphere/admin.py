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
        "author",
        "display_categories",
        "status",
        "is_premium",
        "is_featured",
        "published_at",
    ]

    list_filter = [
        "status",
        "is_premium",
        "is_featured",
        "categories",
        "tags",
    ]

    search_fields = [
        "title",
        "author",
        "excerpt",
        "content",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    filter_horizontal = [
        "categories",
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
                    "author",
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
                    "categories",
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

    @admin.display(description="Kategorie")
    def display_categories(self, article):
        return ", ".join(
            category.name
            for category in article.categories.all()
        )