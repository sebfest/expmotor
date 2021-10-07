from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html

from .models import Experiment, Session, Participant


class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    can_delete = True
    fields = (
        'date',
        'time',
        'place',
        'max_subjects',
        'registrations',
    )
    readonly_fields = ('registrations',)


class ExperimentAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'name',
        'created_date',
        'modified_date',
        'slots',
        'registrations',
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
        ('Confirmation', {
            'fields': ['confirmation_request'],
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


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1
    can_delete = True
    fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
    )


class SessionAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'date',
        'time',
        'place',
        'max_subjects',
        'participant_count',
        'get_object_link',
        'is_active',
    )
    ordering = ('-created_date',)
    actions_on_top = True
    actions_on_bottom = False
    readonly_fields = (
        'created_date',
        'activation_date',
        'modified_date',
        'experiment',
    )
    fields = (
        'experiment',
        'max_subjects',
        'date',
        'time',
        'place',
    )
    inlines = [ParticipantInline]

    @admin.action(description='View on site')
    def get_object_link(self, session: Session) -> str:
        item_url = session.get_absolute_url()
        return format_html('<a href="{url}">Open</a>', url=item_url)

    @admin.display(description='Participants registered.')
    def participant_count(self, session: Session) -> str:
        return format_html('{number}', number=session.participants.count())


class ParticipantAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = (
        'first_name',
        'last_name',
        'email',
        'is_active',
    )
    ordering = ('-created_date',)
    actions_on_top = True
    actions_on_bottom = False
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
        'email',
        'is_active',
    )

    @admin.action(description='View on site')
    def get_object_link(self, participant: Participant) -> str:
        item_url = participant.get_absolute_url()
        return format_html('<a href="{url}">Open</a>', url=item_url)


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Participant, ParticipantAdmin)
