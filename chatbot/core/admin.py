from django.contrib import admin
from chatterbot.ext.django_chatterbot.model_admin import StatementAdmin, TagAdmin
from chatbot.core.models import Statement, Tag


admin.site.register(Statement, StatementAdmin)
admin.site.register(Tag, TagAdmin)