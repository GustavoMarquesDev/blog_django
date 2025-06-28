# 📝 Blog Django

&#x20;

## Sobre o projeto

Este é um blog desenvolvido com Django, Docker e PostgreSQL. A aplicação permite a criação, edição e publicação de posts através do painel administrativo. É possível também criar páginas informativas como "Sobre" e outras seções personalizadas para enriquecer o conteúdo do blog.

## Tecnologias utilizadas

| Tecnologia | Versão                          |
| ---------- | ------------------------------- |
| Python     | 3.11+                           |
| Django     | 4.2+                            |
| Docker     | 20.10+                          |
| PostgreSQL | 15+                             |
| Summernote | 0.8+                            |
| Pillow     | 11.2+                           |

## Funcionalidades

- Cadastro e edição de posts via admin
- Criação de páginas estáticas (ex: Sobre)
- Editor de texto rico com Summernote
- Deploy local via Docker

## Como rodar o projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/GustavoMarquesDev/blog_django.git
   cd blog_django
   ```

2. Configure o ambiente:

   - Dentro da pasta `dotenv_files`, crie um arquivo `.env` baseado no `.env-example`.

3. Inicie os containers:

   ```bash
   docker-compose up --build
   ```

4. Crie o superusuário do Django:

   ```bash
   docker-compose run --rm djangoapp python manage.py createsuperuser
   ```

5. Acesse a aplicação:

   - Site: [http://localhost:8000](http://localhost:8000)
   - Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

## Autor

[Gustavo Marques](https://github.com/GustavoMarquesDev)
