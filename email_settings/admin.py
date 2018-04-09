from django.contrib import admin

from email_settings.models import EmailSetting


@admin.register(EmailSetting)
class EmailSettingAdmin(admin.ModelAdmin):
     list_display = ('name', 'active', 'tag')
