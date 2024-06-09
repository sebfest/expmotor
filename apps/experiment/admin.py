from django.contrib import admin
from django.utils.html import format_html

from .models import Experiment, Session, Registration


class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    can_delete = True
    fields = (
        'date',
        'time',
        'place',
        'max_subjects',
        'active_registrations',
    )
    readonly_fields = ('active_registrations',)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'manager',
        'created_date',
        'modified_date',
        'slots',
        'active_registrations',
        'is_active',
        'get_object_link',
    )
    search_fields = ('name',)
    ordering = ('-created_date',)
    actions_on_top = True
    actions_on_bottom = False
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        'created_date',
        'activation_date',
        'modified_date',
    )
    inlines = [SessionInline]
    fieldsets = [
        ('Main', {
            'fields': (
                'name',
                'manager',
                'email',
                'phone',
            )
        }),
        ('Registration', {
            'fields': ['registration_help'],
            'classes': ('collapse',),
        }),
        ('Instructions', {
            'fields': ['final_instructions'],
            'classes': ('collapse',),
        }),
        ('Info', {
            'fields': (
                'slug',
                'created_date',
                'modified_date',
                'activation_date',
            ),
            'classes': ['collapse'],
        }),
    ]

    @admin.action(description='View on site')
    def get_object_link(self, experiment: Experiment) -> str:
        item_url = experiment.get_absolute_url()
        return format_html('<a href="{url}">Open</a>', url=item_url)


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 1
    can_delete = True
    fields = (
        'last_name',
        'first_name',
        'phone',
        'email',
        'confirmed_email',
        'is_active',
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_select_related = True
    list_per_page = 20
    list_display = (
        'date',
        'time',
        'place',
        'max_subjects',
        'active_registrations',
        'is_active',
    )
    ordering = ('date',)
    date_hierarchy = 'date'
    actions_on_top = True
    actions_on_bottom = False
    list_filter = (
        'date',
        'is_active',
    )
    view_on_site = False
    fields = (
        'experiment',
        'max_subjects',
        'date',
        'time',
        'place',
        'is_active',
    )
    readonly_fields = (
        'experiment',
        'created_date',
        'activation_date',
        'modified_date',
    )
    inlines = [RegistrationInline]

    @admin.display(description='Registrations.')
    def active_registrations(self, session: Session) -> str:
        return format_html('{registrations}', registrations=session.active_registrations)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_select_related = False
    list_per_page = 20
    list_display = (
        'last_name',
        'first_name',
        'phone',
        'email',
        'confirmed_email',
        'is_active',
    )
    ordering = ('last_name',)
    actions_on_top = True
    actions_on_bottom = False
    search_fields = ['last_name']
    date_hierarchy = 'created_date'
    list_filter = (
        'session__date',
        'confirmed_email',
        'is_active',
    )
    view_on_site = False
    readonly_fields = (
        'session',
        'created_date',
        'activation_date',
        'modified_date',
    )
    fields = (
        'session',
        'first_name',
        'last_name',
        'phone',
        'email',
        'confirmed_email',
        'is_active',
    )


