from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    date_hierarchy = 'date_joined'
    list_display = ('get_full_name', 'username', 'email', 'phone', 'date_joined', 'user_type',)
    list_filter = ('user_type', 'date_joined',)
    exclude = ('user_permissions',)
    fields = ('first_name', 'last_name', 'username', 'password', 'phone', 'email', 'city', 'groups',)

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.admin_order_field = 'user__first_Name'
    get_full_name.short_description = 'Nome Completo'

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)
