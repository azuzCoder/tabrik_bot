from django.contrib import admin

from api.bot_app.models import *

admin.site.register(BotUser)
admin.site.register(JoinedGroup)
admin.site.register(Birthday)