from django.contrib import admin
from .models import Todos

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Todos, TodoAdmin)
