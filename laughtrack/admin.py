from django.contrib import admin

from .models import Event,Comment,Comedian

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Comedian)

# Register your models here.
