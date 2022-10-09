from django.contrib.admin import ModelAdmin, register

from .models import Subscribe, User


@register(User)
class UserAdmin(ModelAdmin):
    """Админка пользователей."""
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


@register(Subscribe)
class SubscribeAdmin(UserAdmin):
    """Админка подписок."""
    list_display = (
        'username',
        'get_subscribe',
    )
    empty_value_display = '-'

    def get_subscribe(self, obj):
        return ',\n'.join([p.username for p in obj.subscribe.all()])
    get_subscribe.short_description = 'подписки'
