from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    search_fields = ['address', 'district']
    date_hierarchy = 'created_at'
    list_display = ('get_full_name', 'get_phone', 'get_email', 'created_at', 'address', 'district',
                    'get_city_and_state', 'modified_at', 'status',)
    list_filter = ('status', 'city__name', 'created_at',)
    actions = ['accept', 'reject', 'pending']
    exclude = ['Permissions']
    READ_ONLY_GROUPS = ("Agente",)

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_email(self, obj):
        return obj.user.email

    def get_phone(self, obj):
        return obj.user.phone

    def get_city_and_state(self, obj):
        return obj.city.__str__()

    get_email.admin_order_field = 'user__email'
    get_email.short_description = 'Email'

    get_phone.admin_order_field = 'user__phone'
    get_phone.short_description = 'Telefone'

    get_full_name.admin_order_field = 'user__first_name'
    get_full_name.short_description = 'Enviado por'

    get_city_and_state.admin_order_field = 'city__name'
    get_city_and_state.short_description = 'Cidade/UF'


class ReadOnlyReportAdmin(ReportAdmin):
    def __init__(self, model, admin_site):
        super(ReadOnlyReportAdmin, self).__init__(model, admin_site)
        self.model = model

    def has_delete_permission(self, request, obj=None):
        return not self._user_is_readonly(request)

    def has_add_permission(self, request, obj=None):
        return not self._user_is_readonly(request)

    def has_change_permission(self, request, obj=None):
        if self._user_is_readonly(request):
            self.readonly_fields = [f.name for f in self.model._meta.fields]
        else:
            self.readonly_fields = ()
        return True

    def get_actions(self, request):
        actions = super(ReadOnlyReportAdmin, self).get_actions(request)
        if self._user_is_readonly(request):
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def _user_is_readonly(self, request):
        user_groups = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser:
            return False
        else:
            for read_only_group in self.READ_ONLY_GROUPS:
                if read_only_group in user_groups:
                    return True
        return False



admin.site.register(Report, ReadOnlyReportAdmin)