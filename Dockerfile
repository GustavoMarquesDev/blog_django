FROM python:3.11.3-alpine3.18
LABEL maintainer="gustavo-marques@hotmail.com"

# Variáveis de ambiente para melhorar comportamento do Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apk update && apk add --no-cache \
    build-base \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    libpng \
    libwebp \
    tiff-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tk-dev \
    harfbuzz-dev \
    fribidi-dev \
    dos2unix

# Copia o código e os scripts para dentro do container
COPY djangoapp /djangoapp
COPY scripts /scripts

# Corrige formato de fim de linha e adiciona permissão de execução nos scripts
RUN dos2unix /scripts/*.sh && chmod +x /scripts/*.sh

# Define o diretório de trabalho
WORKDIR /djangoapp

# Expõe a porta usada pelo Django
EXPOSE 8000

# Cria ambiente virtual, instala dependências e configura usuário e diretórios
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /djangoapp/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static /data/web/media && \
    chown -R duser:duser /venv /data/web/static /data/web/media && \
    chmod -R 755 /data/web/static /data/web/media

# Ajusta o PATH para incluir scripts e ambiente virtual
ENV PATH="/scripts:/venv/bin:$PATH"

# Usa o usuário limitado para rodar o container
USER duser

# Comando padrão de inicialização do container
CMD ["commands.sh"]
