FROM python:3.11.3-alpine3.18
LABEL maintainer="gustavo-marques@hotmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema necessárias para Pillow
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
    fribidi-dev

COPY djangoapp /djangoapp
COPY scripts /scripts

WORKDIR /djangoapp
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /djangoapp/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /data/web/static && \
    chown -R duser:duser /data/web/media && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["commands.sh"]
