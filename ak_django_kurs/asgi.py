"""
ASGI config for ak_django_kurs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# Ак для ассинхронных веб серверов и приложений 

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak_django_kurs.settings')

application = get_asgi_application()
