from rest_framework import serializers

from .models import Article, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "excerpt",
            "image_url",
            "category",
            "tags",
            "read_time_minutes",
            "is_premium",
            "is_featured",
            "published_at",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    content = serializers.SerializerMethodField()
    has_access = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "excerpt",
            "content",
            "image_url",
            "category",
            "tags",
            "read_time_minutes",
            "is_premium",
            "is_featured",
            "has_access",
            "published_at",
        ]

    def get_has_access(self, article):
        # Na razie nie mamy subskrypcji.
        # Artykuły darmowe są dostępne, premium są zablokowane.
        return not article.is_premium

    def get_content(self, article):
        if article.is_premium:
            return None

        return article.content