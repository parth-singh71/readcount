from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'gender', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_active', 'date_of_birth', 'gender', 'is_staff')
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Other Details',
            {
                'fields': (
                    'date_of_birth', 'gender',
                ),
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, CustomUserAdmin)
