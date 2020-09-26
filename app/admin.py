from django.contrib import admin
from .models import Restoran, UserProfile
# Register your models here.

class RestoranAdmin(admin.ModelAdmin):
    fields = ('name', 'image', 'tables')

admin.site.register(Restoran, RestoranAdmin)


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'mobile', 'avatar', 'status', 'restoran')

admin.site.register(UserProfile, UserAdmin)