from django.contrib import admin

from .models import *

# Для регистрации модели добавить её в models
models = [Equipment, Contact, GroupAccounting, UserAccounting
]

for model in models:
    admin.site.register(model)