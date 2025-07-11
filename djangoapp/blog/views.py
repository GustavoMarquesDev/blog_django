from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from blog.models import Post, Page, Tag
from blog.forms import PostForm, RegisterForm


PER_PAGE = 9


class PostListView(ListView):
    model = Post
    paginate_by = PER_PAGE
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = '-pk'
    queryset = Post.objects.get_published()   # type: ignore

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)

    #     return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


# def index(request):
#     posts = Post.objects.get_published()  # type: ignore

#     search_value = request.GET.get("search", "").strip()

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#             'search_value': search_value,
#         }
#     )

class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"

        page_title = f"Posts by {user_full_name} - "

        context.update({
            'page_title': page_title,
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            created_by__pk=self._temp_context['user'].pk)

        return queryset

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404("User not found")

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()

#     if user is None:
#         raise Http404("User not found")

#     posts = Post.objects.get_published().filter(  # type: ignore
#         created_by__pk=author_pk)

#     user_full_name = user.username

#     if user.first_name:
#         user_full_name = f"{user.first_name} {user.last_name}"

#     page_title = f"Posts by {user_full_name} - "

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        page_title = (
            f'{self.object_list[0].category.name}'  # type: ignore
            '- Category - '
        )

        context.update({
            'page_title': page_title,
        })

        return context


# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)  # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(posts) == 0:
#         raise Http404("Category not found")

#     page_title = f"{posts[0].category.name} - Category"

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        page_title = f'{self.tag.name} - Tag - '

        context.update({
            'page_title': page_title,
        })

        return context


# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)  # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     tag = get_object_or_404(Tag, slug=slug)

#     if len(page_obj) == 0:
#         raise Http404("Tag not found")

#     page_title = f"{tag.name} - Tag -"

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        search_value = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) |
            Q(tags__name__icontains=search_value) |
            Q(category__name__icontains=search_value)
        )[:PER_PAGE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self._search_value

        context.update({
            'search_value': search_value,
            'page_title': f'{search_value[:30]} - Search -',
        })

        return context

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')

        return super().get(request, *args, **kwargs)


# def search(request):
#     search_value = request.GET.get("search", "").strip()

#     posts = (
#         Post.objects.get_published()  # type: ignore
#         .filter(
#             Q(title__icontains=search_value) |
#             Q(excerpt__icontains=search_value) |
#             Q(content__icontains=search_value)
#         )[:PER_PAGE]
#     )

#     page_title = f'{search_value[:30]} - Search -'

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} - Página - "  # type: ignore
        context.update({
            'page_title': page_title,
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


# def page(request, slug):
#     page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

#     if page_obj is None:
#         raise Http404("Page not found")

#     page_title = f"{page_obj.title} - "

#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page': page_obj,
#             'page_title': page_title,
#         }
#     )


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/pages/post.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f"{post.title} - Post - "  # type: ignore
        context.update({
            'page_title': page_title,
        })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


# def post(request, slug):
#     post_obj = Post.objects.get_published().filter(slug=slug).first()  # type: ignore

#     if post_obj is None:
#         raise Http404("Post not found")

#     page_title = f"{post_obj.title} - Post - "

#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post_obj,
#             'page_title': page_title,
#         }
#     )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/pages/post_create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user

        messages.success(
            self.request,
            'Post criado com sucesso!'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Criar Post - '
        return context


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'blog/pages/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
