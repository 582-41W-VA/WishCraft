from django.contrib import admin
from . import models

admin.site.register(models.Card)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
