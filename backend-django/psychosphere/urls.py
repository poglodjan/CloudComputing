from django.urls import path

from .views import (
    ArticleDetailView,
    ArticleListView,
    CategoryListView,
    TagListView,
)


app_name = "psychosphere"


urlpatterns = [
    path(
        "articles/",
        ArticleListView.as_view(),
        name="article-list",
    ),
    path(
        "articles/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article-detail",
    ),
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list",
    ),
    path(
        "tags/",
        TagListView.as_view(),
        name="tag-list",
    ),
]