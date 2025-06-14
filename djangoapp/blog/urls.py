from django.urls import path

from blog.views import (
    PostListView,
    CreatedByListView,
    CategoryListView,
    TagListView,
    page,
    post,
    search,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path("post/<slug:slug>/", post, name="post"),
    path("page/<slug:slug>/", page, name="page"),
    path(
        "created_by/<int:author_pk>/",
        CreatedByListView.as_view(),
        name="created_by"
    ),
    path("category/<slug:slug>/", CategoryListView.as_view(), name="category"),
    path("tag/<slug:slug>/", TagListView.as_view(), name="tag"),
    path("search/", search, name="search"),

]
