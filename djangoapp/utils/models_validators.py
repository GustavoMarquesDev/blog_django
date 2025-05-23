from django.core.exceptions import ValidationError


def validate_png(image):
    if not image.name.lower().endswith(('.png', '.ico')):
        raise ValidationError('O arquivo deve ser um PNG ou ICO.')
