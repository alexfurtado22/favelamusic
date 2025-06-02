from django.contrib import admin

from app.models import Artist, Producer, UserProfile

admin.site.register(UserProfile)
admin.site.register(Producer)
admin.site.register(Artist)
