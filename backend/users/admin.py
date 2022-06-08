from django.contrib.admin import ModelAdmin, register

from .models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('email', 'username', )
    ordering = ('date_joined',)
    empty_value_display = '-'
