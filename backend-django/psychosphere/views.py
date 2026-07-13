from django.db.models import Q
from django.utils import timezone

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from .models import Article, Category, Tag
from .serializers import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    CategorySerializer,
    TagSerializer,
)


class PublicPsychosphereViewMixin:
    permission_classes = [AllowAny]

    # PsychSphere jest na razie całkowicie publiczna.
    # Nie uruchamiamy FirebaseAuthentication dla tych endpointów.
    authentication_classes = []


class ArticleListView(PublicPsychosphereViewMixin, ListAPIView):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        queryset = (
            Article.objects
            .filter(
                status=Article.Status.PUBLISHED,
                published_at__lte=timezone.now(),
            )
            .select_related("category")
            .prefetch_related("tags")
        )

        search = self.request.query_params.get("search", "").strip()
        category = self.request.query_params.get("category", "").strip()
        tag = self.request.query_params.get("tag", "").strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(excerpt__icontains=search)
                | Q(content__icontains=search)
                | Q(category__name__icontains=search)
                | Q(tags__name__icontains=search)
            ).distinct()

        if category:
            queryset = queryset.filter(category__slug=category)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset


class ArticleDetailView(
    PublicPsychosphereViewMixin,
    RetrieveAPIView,
):
    serializer_class = ArticleDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Article.objects
            .filter(
                status=Article.Status.PUBLISHED,
                published_at__lte=timezone.now(),
            )
            .select_related("category")
            .prefetch_related("tags")
        )


class CategoryListView(
    PublicPsychosphereViewMixin,
    ListAPIView,
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TagListView(
    PublicPsychosphereViewMixin,
    ListAPIView,
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()