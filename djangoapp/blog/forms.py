from django import forms
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'excerpt',
            'content',
            'cover',
            'cover_in_post_content',
            'is_published',
            'category',
            'tags',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do post'
            }),
            'excerpt': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite um resumo do post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Digite o conteúdo do post'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'cover_in_post_content': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cover'].required = False
        self.fields['category'].required = False
        self.fields['tags'].required = False
        self.fields['is_published'].required = False
        self.fields['cover_in_post_content'].required = False


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Senha')
    password2 = forms.CharField(
        label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            self.add_error('password2', 'As senhas não coincidem.')
        return cleaned_data
