from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django_summernote.models import AbstractAttachment

from utils.images import resize_image
from utils.rands import slugfy_new


class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default=None,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name, k=4)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default=None,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name, k=4)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=65)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default=None,
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        default=False,
        help_text='Marque para exibir a página publicamente'
    )
    content = models.TextField()

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:page', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title, k=4)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(
        max_length=65,
        help_text='Título do post (máx. 65 caracteres)'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        default=None,
        null=True,
        blank=True,
    )
    excerpt = models.CharField(
        max_length=150,
        help_text='Breve descrição do post (máx. 150 caracteres)'
    )
    is_published = models.BooleanField(
        default=False,
        help_text='Marque para exibir o post publicamente'
    )
    content = models.TextField()
    cover = models.ImageField(
        upload_to='posts/%Y/%m/', blank=True, default='',)
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Exibir a capa dentro do post'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='post_created_by',
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='page_updated_by',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        default='',
        help_text='Selecione as tags relacionadas ao post'
    )

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title, k=4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 70)

        return super_save

    def __str__(self):
        return self.title
