from django.contrib.admin import ModelAdmin, site
from users.models import Subscription, User


class UserAdmin(ModelAdmin):
    list_display = ('pk',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_active',
                    'last_login',
                    )
    list_editable = ('is_active',)
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscriptionAdmin(ModelAdmin):
    list_display = ('pk',
                    'user',
                    'author',
                    )
    list_editable = ('user', 'author',)
    list_filter = ('user', 'author')


site.register(User, UserAdmin)
site.register(Subscription, SubscriptionAdmin)
